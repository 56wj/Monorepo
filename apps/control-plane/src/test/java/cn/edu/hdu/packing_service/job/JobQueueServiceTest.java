package cn.edu.hdu.packing_service.job;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class JobQueueServiceTest {

    @Test
    void retryDelayUsesBoundedExponentialBackoff() {
        JobQueueProperties properties = new JobQueueProperties();
        properties.setRetryBaseSeconds(10);
        JobQueueService service = new JobQueueService(null, properties, null, null);

        assertEquals(10, service.retryDelaySeconds(1));
        assertEquals(20, service.retryDelaySeconds(2));
        assertEquals(40, service.retryDelaySeconds(3));
        assertEquals(3600, service.retryDelaySeconds(20));
    }
}
