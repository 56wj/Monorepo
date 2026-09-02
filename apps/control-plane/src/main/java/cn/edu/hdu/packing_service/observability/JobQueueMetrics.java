package cn.edu.hdu.packing_service.observability;

import cn.edu.hdu.packing_service.job.JobStatusCount;
import cn.edu.hdu.packing_service.job.JobStatus;
import cn.edu.hdu.packing_service.job.PackingJob;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.MultiGauge;
import io.micrometer.core.instrument.Tags;
import io.micrometer.core.instrument.Timer;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Component
public class JobQueueMetrics {
    private final MeterRegistry registry;
    private final MultiGauge queueDepth;

    public JobQueueMetrics(MeterRegistry registry) {
        this.registry = registry;
        this.queueDepth = MultiGauge.builder("packing.job.queue.depth")
                .description("Current durable job count by state")
                .register(registry);
    }

    public void enqueued(PackingJob job) {
        counter("packing.jobs.enqueued", "job_type", job.getJobType()).increment();
    }

    public void claimed(PackingJob job, LocalDateTime claimedAt) {
        counter("packing.jobs.claimed", "job_type", job.getJobType()).increment();
        recordDuration("packing.job.queue.delay", job, job.getCreatedAt(), claimedAt);
        registry.summary("packing.job.attempt", "job_type", job.getJobType()).record(job.getAttempt());
    }

    public void heartbeat() {
        counter("packing.job.heartbeats").increment();
    }

    public void completed(PackingJob job, String outcome, LocalDateTime completedAt) {
        counter("packing.jobs.completed", "job_type", job.getJobType(), "outcome", outcome).increment();
        recordDuration("packing.job.execution", job, job.getStartedAt(), completedAt);
    }

    public void retried(PackingJob job, String reason) {
        counter("packing.jobs.retried", "job_type", job.getJobType(), "reason", reason).increment();
    }

    public void leaseExpired(PackingJob job) {
        counter("packing.job.lease.expired", "job_type", job.getJobType()).increment();
    }

    public void refreshQueueDepth(List<JobStatusCount> counts) {
        Map<String, Long> byStatus = new HashMap<>();
        for (JobStatusCount count : counts) byStatus.put(count.getStatus(), count.getCount());
        List<MultiGauge.Row<?>> rows = new ArrayList<>();
        for (JobStatus status : JobStatus.values()) {
            rows.add(MultiGauge.Row.of(Tags.of("status", status.name()),
                    byStatus.getOrDefault(status.name(), 0L)));
        }
        queueDepth.register(rows, true);
    }

    private Counter counter(String name, String... tags) {
        return Counter.builder(name).tags(tags).register(registry);
    }

    private void recordDuration(String name, PackingJob job, LocalDateTime start, LocalDateTime end) {
        if (start == null || end == null || end.isBefore(start)) return;
        long nanos = Duration.between(start, end).toNanos();
        Timer.builder(name)
                .description("Packing job lifecycle latency")
                .tag("job_type", job.getJobType())
                .publishPercentileHistogram()
                .register(registry)
                .record(nanos, TimeUnit.NANOSECONDS);
    }
}
