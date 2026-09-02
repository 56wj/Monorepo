package cn.edu.hdu.packing_service.observability;

import cn.edu.hdu.packing_service.job.PackingJobMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class JobMetricsRefresher {
    private static final Logger LOG = LoggerFactory.getLogger(JobMetricsRefresher.class);
    private final PackingJobMapper mapper;
    private final JobQueueMetrics metrics;

    public JobMetricsRefresher(PackingJobMapper mapper, JobQueueMetrics metrics) {
        this.mapper = mapper;
        this.metrics = metrics;
    }

    @Scheduled(fixedDelayString = "${observability.queue-refresh-ms:15000}")
    public void refresh() {
        try {
            metrics.refreshQueueDepth(mapper.countByStatus());
        } catch (RuntimeException error) {
            LOG.warn("queue_metric_refresh_failed error={}", error.toString());
        }
    }
}
