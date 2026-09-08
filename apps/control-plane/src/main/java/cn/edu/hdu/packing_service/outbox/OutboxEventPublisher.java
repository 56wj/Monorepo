package cn.edu.hdu.packing_service.outbox;

public interface OutboxEventPublisher {
    void publish(OutboxEvent event) throws Exception;
}
