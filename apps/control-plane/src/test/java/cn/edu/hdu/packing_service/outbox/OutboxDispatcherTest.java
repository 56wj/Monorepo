package cn.edu.hdu.packing_service.outbox;

import org.junit.jupiter.api.Test;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class OutboxDispatcherTest {

    @Test
    void publishesAndAcknowledgesAClaimedEvent() throws Exception {
        OutboxService service = mock(OutboxService.class);
        OutboxEventPublisher publisher = mock(OutboxEventPublisher.class);
        OutboxEvent event = event();
        when(service.claimNext(anyString())).thenReturn(event, null);

        new OutboxDispatcher(service, publisher, properties()).dispatchBatch();

        verify(publisher).publish(event);
        verify(service).markPublished("event-1", "lease-1");
    }

    @Test
    void schedulesRetryWhenPublisherFails() throws Exception {
        OutboxService service = mock(OutboxService.class);
        OutboxEventPublisher publisher = mock(OutboxEventPublisher.class);
        OutboxEvent event = event();
        RuntimeException failure = new RuntimeException("broken channel");
        when(service.claimNext(anyString())).thenReturn(event, null);
        doThrow(failure).when(publisher).publish(event);

        new OutboxDispatcher(service, publisher, properties()).dispatchBatch();

        verify(service).markFailed("event-1", "lease-1", failure);
    }

    private OutboxProperties properties() {
        OutboxProperties properties = new OutboxProperties();
        properties.setDispatchBatchSize(10);
        return properties;
    }

    private OutboxEvent event() {
        OutboxEvent event = new OutboxEvent();
        event.setEventId("event-1");
        event.setEventType("PALLET_FIRST_COMPLETED");
        event.setLeaseToken("lease-1");
        event.setAttempt(1);
        return event;
    }
}
