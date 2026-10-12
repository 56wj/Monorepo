package cn.edu.hdu.packing_service.notification;

import org.flywaydb.core.Flyway;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.condition.EnabledIfEnvironmentVariable;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.transaction.support.TransactionTemplate;

import java.sql.Connection;
import java.sql.ResultSet;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/** Opt-in integration tests. Every test creates and drops only its own random schema. */
@EnabledIfEnvironmentVariable(named = "NOTIFICATION_TEST_MYSQL_URL", matches = ".+")
class TaskNotificationMigrationTest {
    private String schema;
    private JdbcTemplate admin;
    private boolean schemaCreated;
    private JdbcTemplate jdbc;
    private DriverManagerDataSource dataSource;

    @BeforeEach void setup() {
        String base = System.getenv("NOTIFICATION_TEST_MYSQL_URL");
        assertTrue(base.endsWith("/"), "Use a JDBC base URL ending with / (no database or parameters)");
        String user = System.getenv().getOrDefault("NOTIFICATION_TEST_MYSQL_USER", "root");
        String password = System.getenv().getOrDefault("NOTIFICATION_TEST_MYSQL_PASSWORD", "");
        schema = "notify_test_" + UUID.randomUUID().toString().replace("-", "");
        admin = new JdbcTemplate(new DriverManagerDataSource(base, user, password));
        admin.execute("CREATE DATABASE " + schema);
        schemaCreated = true;
        dataSource = new DriverManagerDataSource(base + schema, user, password);
        jdbc = new JdbcTemplate(dataSource);
    }

    @AfterEach void cleanup() {
        if (schemaCreated) admin.execute("DROP DATABASE IF EXISTS " + schema);
    }

    @Test void freshInstallEndsAtV5WithoutNotificationStore() {
        Flyway flyway = Flyway.configure().dataSource(dataSource).load();
        flyway.migrate();
        flyway.validate();
        assertEquals("5", flyway.info().current().getVersion().toString());
        assertEquals(0, tableCount("packing_outbox_event"));
        assertEquals(1, tableCount("packing_job"));
    }

    @Test void upgradePreservesResultsAndRealTransactionsNotifyOnlyAfterCommit() throws Exception {
        Flyway.configure().dataSource(dataSource).target("4").load().migrate();
        assertEquals(1, tableCount("packing_outbox_event"));
        jdbc.update("INSERT INTO packing_job(public_id,task_id,job_type,status,payload_json," +
                "available_at,idempotency_key,created_at,updated_at,result_json) " +
                "VALUES('job-42',42,'PALLET_FIRST','RUNNING','{}',NOW(),'test-42',NOW(),NOW(),NULL)");
        Flyway upgrade = Flyway.configure().dataSource(dataSource).load();
        upgrade.migrate();
        upgrade.validate();
        assertEquals(0, tableCount("packing_outbox_event"));
        assertEquals(1, jdbc.queryForObject("SELECT COUNT(*) FROM packing_job", Integer.class));

        TaskNotificationSender sender = mock(TaskNotificationSender.class);
        TaskNotificationService notifications = new TaskNotificationService(sender, Runnable::run);
        TransactionTemplate transaction = new TransactionTemplate(new DataSourceTransactionManager(dataSource));
        doAnswer(call -> {
            // A separate connection must already observe the committed result when notified.
            try (Connection connection = dataSource.getConnection();
                 ResultSet rows = connection.createStatement().executeQuery("SELECT status FROM packing_job WHERE public_id='job-42'")) {
                assertTrue(rows.next());
                assertEquals("SUCCEEDED", rows.getString(1));
            }
            return null;
        }).when(sender).send("9", 42);
        transaction.execute(status -> {
            jdbc.update("UPDATE packing_job SET status='SUCCEEDED',result_json='{\"result\":\"[]\"}' WHERE public_id='job-42'");
            notifications.notifyAfterCommit("9", 42);
            verifyNoInteractions(sender);
            return null;
        });
        verify(sender).send("9", 42);
        assertEquals("{\"result\":\"[]\"}", jdbc.queryForObject("SELECT result_json FROM packing_job", String.class));
        reset(sender);
        transaction.execute(status -> {
            jdbc.update("UPDATE packing_job SET status='DEAD_LETTER'");
            notifications.notifyAfterCommit("9", 42);
            status.setRollbackOnly();
            return null;
        });
        verifyNoInteractions(sender);
        assertEquals("SUCCEEDED", jdbc.queryForObject("SELECT status FROM packing_job", String.class));
    }

    private int tableCount(String name) {
        return jdbc.queryForObject("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=? AND table_name=?",
                Integer.class, schema, name);
    }
}
