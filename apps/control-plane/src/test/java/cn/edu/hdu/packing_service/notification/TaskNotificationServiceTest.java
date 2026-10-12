package cn.edu.hdu.packing_service.notification;

import org.junit.jupiter.api.Test;
import org.springframework.transaction.TransactionDefinition;
import org.springframework.transaction.support.AbstractPlatformTransactionManager;
import org.springframework.transaction.support.DefaultTransactionStatus;
import org.springframework.transaction.support.TransactionTemplate;

import java.io.IOException;
import java.util.concurrent.Executor;
import java.util.concurrent.RejectedExecutionException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class TaskNotificationServiceTest {
    private final TaskNotificationSender sender = mock(TaskNotificationSender.class);
    private final TaskNotificationService service = new TaskNotificationService(sender, Runnable::run);
    private final TransactionTemplate transaction = new TransactionTemplate(new TestTransactionManager());

    @Test
    void sendsOnlyAfterSuccessfulCommit() throws Exception {
        transaction.execute(status -> {
            service.notifyAfterCommit("9", 42);
            verifyNoInteractions(sender);
            return null;
        });
        verify(sender).send("9", 42);
    }

    @Test
    void rollbackNeverNotifies() {
        transaction.execute(status -> {
            service.notifyAfterCommit("9", 42);
            status.setRollbackOnly();
            return null;
        });
        verifyNoInteractions(sender);
    }

    @Test
    void businessFailureNeverNotifies() {
        assertThrows(IllegalStateException.class, () -> transaction.execute(status -> {
            service.notifyAfterCommit("9", 42);
            throw new IllegalStateException("job update conflict");
        }));
        verifyNoInteractions(sender);
    }

    @Test
    void networkFailureDoesNotFailCommittedJob() throws Exception {
        doThrow(new IOException("disconnected")).when(sender).send("9", 42);
        assertDoesNotThrow(() -> transaction.execute(status -> {
            service.notifyAfterCommit("9", 42);
            return null;
        }));
        verify(sender).send("9", 42);
    }

    @Test
    void executorSaturationDoesNotFailCommittedJob() {
        Executor rejected = runnable -> { throw new RejectedExecutionException("full"); };
        TaskNotificationService saturated = new TaskNotificationService(sender, rejected);
        assertDoesNotThrow(() -> transaction.execute(status -> {
            saturated.notifyAfterCommit("9", 42);
            return null;
        }));
        verifyNoInteractions(sender);
    }

    @Test
    void rejectsCallsWithoutTransaction() {
        assertThrows(IllegalStateException.class, () -> service.notifyAfterCommit("9", 42));
        verifyNoInteractions(sender);
    }

    private static class TestTransactionManager extends AbstractPlatformTransactionManager {
        protected Object doGetTransaction() { return new Object(); }
        protected void doBegin(Object tx, TransactionDefinition definition) { }
        protected void doCommit(DefaultTransactionStatus status) { }
        protected void doRollback(DefaultTransactionStatus status) { }
    }
}
