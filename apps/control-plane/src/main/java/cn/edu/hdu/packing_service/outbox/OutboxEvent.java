package cn.edu.hdu.packing_service.outbox;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class OutboxEvent {
    private Long id;
    private String eventId;
    private String deduplicationKey;
    private String aggregateType;
    private String aggregateId;
    private String eventType;
    private String userId;
    private String traceId;
    private String payloadJson;
    private String status;
    private Integer attempt;
    private Integer maxAttempts;
    private LocalDateTime availableAt;
    private String leaseOwner;
    private String leaseToken;
    private LocalDateTime leaseExpiresAt;
    private String lastError;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime publishedAt;
    private Integer version;

    public OutboxStatus statusEnum() {
        return OutboxStatus.valueOf(status);
    }
}
