package cn.edu.hdu.packing_service.outbox;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class OutboxMetricsRefresher {
    private static final Logger LOG = LoggerFactory.getLogger(OutboxMetricsRefresher.class);
    private final OutboxEventMapper mapper;
    private final OutboxMetrics metrics;

    public OutboxMetricsRefresher(OutboxEventMapper mapper, OutboxMetrics metrics) {
        this.mapper = mapper;
        this.metrics = metrics;
    }

    @Scheduled(fixedDelayString = "${observability.queue-refresh-ms:15000}")
    public void refresh() {
        try {
            metrics.refreshDepth(mapper.countByStatus());
        } catch (RuntimeException error) {
            LOG.warn("outbox_metric_refresh_failed error={}", error.toString());
        }
    }
}
