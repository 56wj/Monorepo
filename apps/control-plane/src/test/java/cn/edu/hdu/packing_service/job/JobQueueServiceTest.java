package cn.edu.hdu.packing_service.job;

import cn.edu.hdu.packing_service.observability.JobQueueMetrics;
import cn.edu.hdu.packing_service.job.dto.ClaimJobRequest;
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.junit.jupiter.api.Test;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class JobQueueServiceTest {

    @Test
    void retryDelayUsesBoundedExponentialBackoff() {
        JobQueueProperties properties = new JobQueueProperties();
        properties.setRetryBaseSeconds(10);
        JobQueueService service = new JobQueueService(null, properties, null, null,
                new JobQueueMetrics(new SimpleMeterRegistry()));

        assertEquals(10, service.retryDelaySeconds(1));
        assertEquals(20, service.retryDelaySeconds(2));
        assertEquals(40, service.retryDelaySeconds(3));
        assertEquals(3600, service.retryDelaySeconds(20));
    }

    @Test
    void claimDoesNotMixLeaseReapingIntoTheClaimTransaction() {
        PackingJobMapper mapper = mock(PackingJobMapper.class);
        when(mapper.lockNextClaimable(any(), any())).thenReturn(null);
        JobQueueProperties properties = new JobQueueProperties();
        JobQueueService service = new JobQueueService(mapper, properties, null, null,
                new JobQueueMetrics(new SimpleMeterRegistry()));
        ClaimJobRequest request = new ClaimJobRequest();
        request.setWorkerId("worker-1");
        request.setCapabilities(Collections.singletonList(JobType.PALLET_FIRST.name()));
        request.setLeaseSeconds(30);

        assertNull(service.claim(request));

        verify(mapper).lockNextClaimable(any(), any());
        verify(mapper, never()).lockExpiredLeases(any(), any(Integer.class));
    }
}
