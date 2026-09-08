package cn.edu.hdu.packing_service.outbox;

import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class OutboxMetricsTest {

    @Test
    void recordsDeliveryLifecycleAndZeroFillsStates() {
        SimpleMeterRegistry registry = new SimpleMeterRegistry();
        OutboxMetrics metrics = new OutboxMetrics(registry);
        OutboxEvent event = new OutboxEvent();
        event.setEventType("PALLET_SECOND_COMPLETED");
        event.setCreatedAt(LocalDateTime.now().minusSeconds(1));
        OutboxStatusCount pending = new OutboxStatusCount();
        pending.setStatus(OutboxStatus.PENDING.name());
        pending.setCount(3L);

        metrics.enqueued(event);
        metrics.published(event, LocalDateTime.now());
        metrics.retried(event, "publish_failure");
        metrics.deadLettered(event, "lease_expired");
        metrics.refreshDepth(Collections.singletonList(pending));

        assertEquals(1.0, registry.get("packing.outbox.events.published").counter().count());
        assertEquals(3.0, registry.get("packing.outbox.depth")
                .tag("status", "PENDING").gauge().value());
        assertEquals(0.0, registry.get("packing.outbox.depth")
                .tag("status", "DEAD_LETTER").gauge().value());
        assertNotNull(registry.find("packing.outbox.publish.delay").timer());
    }
}
