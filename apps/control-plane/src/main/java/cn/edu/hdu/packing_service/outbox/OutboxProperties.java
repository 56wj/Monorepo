package cn.edu.hdu.packing_service.outbox;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "outbox")
@Data
public class OutboxProperties {
    private int leaseSeconds = 30;
    private int maxAttempts = 8;
    private int retryBaseSeconds = 2;
    private int dispatchBatchSize = 50;
    private int reaperBatchSize = 100;
}
