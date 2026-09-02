package cn.edu.hdu.packing_service.job;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "job-queue")
@Data
public class JobQueueProperties {
    private String workerToken;
    private int defaultLeaseSeconds = 90;
    private int maxLeaseSeconds = 300;
    private int maxAttempts = 3;
    private int retryBaseSeconds = 10;
    private int reaperBatchSize = 100;
}
