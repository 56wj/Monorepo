package cn.edu.hdu.packing_service.notification;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;

import java.util.concurrent.Executor;

/** Best-effort wakeup only. Durable task queries recover missed notifications. */
@Service
public class TaskNotificationService {
    private static final Logger LOG = LoggerFactory.getLogger(TaskNotificationService.class);
    private final TaskNotificationSender sender;
    private final Executor executor;

    public TaskNotificationService(TaskNotificationSender sender,
                                   @Qualifier("taskNotificationExecutor") Executor executor) {
        this.sender = sender;
        this.executor = executor;
    }

    public void notifyAfterCommit(String userId, Integer taskId) {
        if (!TransactionSynchronizationManager.isActualTransactionActive() ||
                !TransactionSynchronizationManager.isSynchronizationActive()) {
            throw new IllegalStateException("Task notifications must be registered inside a transaction");
        }
        TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
            @Override
            public void afterCommit() {
                try {
                    executor.execute(() -> {
                        try {
                            sender.send(userId, taskId);
                        } catch (Exception error) {
                            LOG.warn("task_notification_failed task_id={} error={}", taskId, error.toString());
                        }
                    });
                } catch (RuntimeException error) {
                    // Saturation/shutdown must not turn an already committed job into a failed callback.
                    LOG.warn("task_notification_skipped task_id={} error={}", taskId, error.toString());
                }
            }
        });
    }
}
