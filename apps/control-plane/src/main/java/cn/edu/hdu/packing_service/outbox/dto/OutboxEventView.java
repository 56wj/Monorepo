package cn.edu.hdu.packing_service.outbox.dto;

import cn.edu.hdu.packing_service.outbox.OutboxEvent;
import com.fasterxml.jackson.databind.JsonNode;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class OutboxEventView {
    private Long cursor;
    private String eventId;
    private String aggregateId;
    private String eventType;
    private String traceId;
    private String status;
    private JsonNode payload;
    private LocalDateTime createdAt;
    private LocalDateTime publishedAt;

    public static OutboxEventView from(OutboxEvent event, JsonNode payload) {
        return new OutboxEventView(event.getId(), event.getEventId(), event.getAggregateId(),
                event.getEventType(), event.getTraceId(), event.getStatus(), payload,
                event.getCreatedAt(), event.getPublishedAt());
    }
}
