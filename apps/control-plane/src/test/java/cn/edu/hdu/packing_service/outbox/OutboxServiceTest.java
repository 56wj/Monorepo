package cn.edu.hdu.packing_service.outbox;

import cn.edu.hdu.packing_service.job.PackingJob;
import cn.edu.hdu.packing_service.pojo.Result;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class OutboxServiceTest {

    @Test
    void enqueueCreatesIdempotentDurableNotificationWithEventId() throws Exception {
        OutboxEventMapper mapper = mock(OutboxEventMapper.class);
        ObjectMapper objectMapper = new ObjectMapper();
        SimpleMeterRegistry registry = new SimpleMeterRegistry();
        OutboxService service = new OutboxService(mapper, properties(), objectMapper,
                new OutboxMetrics(registry));
        doAnswer(invocation -> {
            OutboxEvent event = invocation.getArgument(0);
            event.setId(7L);
            return 1;
        }).when(mapper).insertIdempotent(any(OutboxEvent.class));

        Map<String, Object> data = new HashMap<>();
        data.put("taskId", 42);
        service.enqueueTaskEvent(job(), "9", "PALLET_FIRST_COMPLETED",
                Result.success(200, "done", data));

        ArgumentCaptor<OutboxEvent> captor = ArgumentCaptor.forClass(OutboxEvent.class);
        verify(mapper).insertIdempotent(captor.capture());
        OutboxEvent event = captor.getValue();
        JsonNode payload = objectMapper.readTree(event.getPayloadJson());

        assertEquals("job-public-1:PALLET_FIRST_COMPLETED", event.getDeduplicationKey());
        assertEquals("PENDING", event.getStatus());
        assertEquals(42, payload.path("data").path("taskId").asInt());
        assertEquals(event.getEventId(), payload.path("data").path("eventId").asText());
        assertEquals(1.0, registry.get("packing.outbox.events.enqueued")
                .tag("event_type", "PALLET_FIRST_COMPLETED").counter().count());
    }

    @Test
    void claimUsesShortDatabaseLeaseAndReturnsClaimedRow() {
        OutboxEventMapper mapper = mock(OutboxEventMapper.class);
        OutboxService service = service(mapper);
        OutboxEvent candidate = event(0, 8);
        candidate.setStatus(OutboxStatus.PENDING.name());
        OutboxEvent claimed = event(1, 8);
        when(mapper.lockNextPublishable(any())).thenReturn(candidate);
        when(mapper.claim(any(), any(), anyString(), anyString(), any(), any())).thenReturn(1);
        when(mapper.findById(7L)).thenReturn(claimed);

        OutboxEvent result = service.claimNext("dispatcher-1");

        assertEquals(OutboxStatus.PUBLISHING.name(), result.getStatus());
        assertNotNull(result.getLeaseToken());
        verify(mapper).claim(any(), any(), anyString(), anyString(), any(), any());
    }

    @Test
    void failedPublicationRetriesThenMovesToDeadLetter() {
        OutboxEventMapper retryMapper = mock(OutboxEventMapper.class);
        OutboxService retryService = service(retryMapper);
        OutboxEvent retryable = event(1, 3);
        when(retryMapper.lockByEventId("event-1")).thenReturn(retryable);
        when(retryMapper.retry(any(), any(), anyString(), any(), anyString(), any())).thenReturn(1);

        retryService.markFailed("event-1", "lease-1", new RuntimeException("offline"));
        verify(retryMapper).retry(any(), any(), anyString(), any(), anyString(), any());

        OutboxEventMapper deadMapper = mock(OutboxEventMapper.class);
        OutboxService deadService = service(deadMapper);
        OutboxEvent exhausted = event(3, 3);
        when(deadMapper.lockByEventId("event-1")).thenReturn(exhausted);
        when(deadMapper.deadLetter(any(), any(), anyString(), anyString(), any())).thenReturn(1);

        deadService.markFailed("event-1", "lease-1", new RuntimeException("offline"));
        verify(deadMapper).deadLetter(any(), any(), anyString(), anyString(), any());
    }

    @Test
    void retryDelayIsExponentialAndBounded() {
        OutboxService service = service(mock(OutboxEventMapper.class));
        assertEquals(2, service.retryDelaySeconds(1));
        assertEquals(4, service.retryDelaySeconds(2));
        assertEquals(2048, service.retryDelaySeconds(20));
    }

    @Test
    void catchupQueryBoundsCursorAndPageSize() {
        OutboxEventMapper mapper = mock(OutboxEventMapper.class);
        when(mapper.listForUserAfter("9", 0, 200)).thenReturn(Collections.emptyList());
        OutboxService service = service(mapper);

        assertTrue(service.listForUserAfter("9", -3, 1000).isEmpty());
        verify(mapper).listForUserAfter("9", 0, 200);
    }

    private OutboxService service(OutboxEventMapper mapper) {
        return new OutboxService(mapper, properties(), new ObjectMapper(),
                new OutboxMetrics(new SimpleMeterRegistry()));
    }

    private OutboxProperties properties() {
        OutboxProperties properties = new OutboxProperties();
        properties.setLeaseSeconds(30);
        properties.setMaxAttempts(8);
        properties.setRetryBaseSeconds(2);
        return properties;
    }

    private PackingJob job() {
        PackingJob job = new PackingJob();
        job.setPublicId("job-public-1");
        job.setTraceId("trace-12345678");
        return job;
    }

    private OutboxEvent event(int attempt, int maxAttempts) {
        OutboxEvent event = new OutboxEvent();
        event.setId(7L);
        event.setEventId("event-1");
        event.setEventType("PALLET_FIRST_COMPLETED");
        event.setStatus(OutboxStatus.PUBLISHING.name());
        event.setAttempt(attempt);
        event.setMaxAttempts(maxAttempts);
        event.setLeaseToken("lease-1");
        event.setLeaseExpiresAt(LocalDateTime.now().plusMinutes(1));
        event.setVersion(2);
        event.setCreatedAt(LocalDateTime.now().minusSeconds(2));
        return event;
    }
}
