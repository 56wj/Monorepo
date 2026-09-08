package cn.edu.hdu.packing_service.outbox;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.lang.management.ManagementFactory;
import java.util.concurrent.atomic.AtomicBoolean;

@Component
public class OutboxDispatcher {
    private static final Logger LOG = LoggerFactory.getLogger(OutboxDispatcher.class);

    private final OutboxService service;
    private final OutboxEventPublisher publisher;
    private final OutboxProperties properties;
    private final String dispatcherId;
    private final AtomicBoolean dispatching = new AtomicBoolean();

    public OutboxDispatcher(OutboxService service,
                            OutboxEventPublisher publisher,
                            OutboxProperties properties) {
        this.service = service;
        this.publisher = publisher;
        this.properties = properties;
        this.dispatcherId = "outbox-" + ManagementFactory.getRuntimeMXBean().getName();
    }

    @Scheduled(fixedDelayString = "${outbox.dispatch-interval-ms:500}")
    public void dispatchBatch() {
        if (!dispatching.compareAndSet(false, true)) return;
        try {
            for (int i = 0; i < Math.max(1, properties.getDispatchBatchSize()); i++) {
                OutboxEvent event = service.claimNext(dispatcherId);
                if (event == null) break;
                try {
                    publisher.publish(event);
                    service.markPublished(event.getEventId(), event.getLeaseToken());
                } catch (Exception error) {
                    LOG.warn("outbox_publish_failed event_id={} event_type={} attempt={} error={}",
                            event.getEventId(), event.getEventType(), event.getAttempt(), error.toString());
                    service.markFailed(event.getEventId(), event.getLeaseToken(), error);
                }
            }
        } finally {
            dispatching.set(false);
        }
    }

    @Scheduled(fixedDelayString = "${outbox.reaper-interval-ms:30000}")
    public void reclaimExpiredLeases() {
        int recovered = service.reclaimExpiredLeases();
        if (recovered > 0) LOG.warn("outbox_expired_leases_recovered count={}", recovered);
    }
}
