package cn.edu.hdu.packing_service.outbox;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.MultiGauge;
import io.micrometer.core.instrument.Tags;
import io.micrometer.core.instrument.Timer;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Component
public class OutboxMetrics {
    private final MeterRegistry registry;
    private final MultiGauge depth;

    public OutboxMetrics(MeterRegistry registry) {
        this.registry = registry;
        this.depth = MultiGauge.builder("packing.outbox.depth")
                .description("Current durable Outbox event count by state")
                .register(registry);
    }

    public void enqueued(OutboxEvent event) {
        counter("packing.outbox.events.enqueued", "event_type", event.getEventType()).increment();
    }

    public void published(OutboxEvent event, LocalDateTime now) {
        counter("packing.outbox.events.published", "event_type", event.getEventType()).increment();
        if (event.getCreatedAt() != null && !now.isBefore(event.getCreatedAt())) {
            long nanos = Duration.between(event.getCreatedAt(), now).toNanos();
            Timer.builder("packing.outbox.publish.delay")
                    .description("Time from event creation to successful publication")
                    .tag("event_type", event.getEventType())
                    .publishPercentileHistogram()
                    .register(registry)
                    .record(nanos, TimeUnit.NANOSECONDS);
        }
    }

    public void retried(OutboxEvent event, String reason) {
        counter("packing.outbox.events.retried", "event_type", event.getEventType(), "reason", reason)
                .increment();
    }

    public void deadLettered(OutboxEvent event, String reason) {
        counter("packing.outbox.events.dead.letter", "event_type", event.getEventType(), "reason", reason)
                .increment();
    }

    public void refreshDepth(List<OutboxStatusCount> counts) {
        Map<String, Long> byStatus = new HashMap<>();
        for (OutboxStatusCount count : counts) byStatus.put(count.getStatus(), count.getCount());
        List<MultiGauge.Row<?>> rows = new ArrayList<>();
        for (OutboxStatus status : OutboxStatus.values()) {
            rows.add(MultiGauge.Row.of(Tags.of("status", status.name()),
                    byStatus.getOrDefault(status.name(), 0L)));
        }
        depth.register(rows, true);
    }

    private Counter counter(String name, String... tags) {
        return Counter.builder(name).tags(tags).register(registry);
    }
}
