package cn.edu.hdu.packing_service.observability;

import cn.edu.hdu.packing_service.job.JobStatusCount;
import cn.edu.hdu.packing_service.job.PackingJob;
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class JobQueueMetricsTest {
    @Test
    void recordsLifecycleAndZeroFillsQueueStates() {
        SimpleMeterRegistry registry = new SimpleMeterRegistry();
        JobQueueMetrics metrics = new JobQueueMetrics(registry);
        PackingJob job = new PackingJob();
        job.setJobType("PALLET_FIRST");
        job.setAttempt(1);
        job.setCreatedAt(LocalDateTime.now().minusSeconds(2));
        job.setStartedAt(LocalDateTime.now().minusSeconds(1));

        metrics.enqueued(job);
        metrics.claimed(job, LocalDateTime.now());
        metrics.completed(job, "succeeded", LocalDateTime.now());

        JobStatusCount queued = new JobStatusCount();
        queued.setStatus("QUEUED");
        queued.setCount(7L);
        metrics.refreshQueueDepth(Collections.singletonList(queued));

        assertEquals(1.0, registry.get("packing.jobs.enqueued").counter().count());
        assertEquals(1.0, registry.get("packing.jobs.completed")
                .tag("outcome", "succeeded").counter().count());
        assertEquals(7.0, registry.get("packing.job.queue.depth")
                .tag("status", "QUEUED").gauge().value());
        assertEquals(0.0, registry.get("packing.job.queue.depth")
                .tag("status", "RUNNING").gauge().value());
        assertNotNull(registry.find("packing.job.queue.delay").timer());
    }
}
