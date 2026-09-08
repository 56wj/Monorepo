package cn.edu.hdu.packing_service.outbox;

import cn.edu.hdu.packing_service.job.PackingJob;
import cn.edu.hdu.packing_service.pojo.Result;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;
import org.springframework.web.server.ResponseStatusException;

import java.time.LocalDateTime;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
public class OutboxService {
    private static final int MAX_ERROR_LENGTH = 1000;

    private final OutboxEventMapper mapper;
    private final OutboxProperties properties;
    private final ObjectMapper objectMapper;
    private final OutboxMetrics metrics;

    public OutboxService(OutboxEventMapper mapper,
                         OutboxProperties properties,
                         ObjectMapper objectMapper,
                         OutboxMetrics metrics) {
        this.mapper = mapper;
        this.properties = properties;
        this.objectMapper = objectMapper;
        this.metrics = metrics;
    }

    /**
     * Joins the caller's transaction. The task/job update and Outbox insert are
     * therefore committed or rolled back together.
     */
    @Transactional
    public OutboxEvent enqueueTaskEvent(PackingJob job,
                                        String userId,
                                        String eventType,
                                        Result<?> notification) {
        LocalDateTime now = LocalDateTime.now();
        String eventId = UUID.randomUUID().toString();

        OutboxEvent event = new OutboxEvent();
        event.setEventId(eventId);
        event.setDeduplicationKey(job.getPublicId() + ":" + eventType);
        event.setAggregateType("PACKING_JOB");
        event.setAggregateId(job.getPublicId());
        event.setEventType(eventType);
        event.setUserId(userId);
        event.setTraceId(job.getTraceId() == null ? "legacy" : job.getTraceId());
        event.setPayloadJson(toJson(withEventId(notification, eventId)));
        event.setStatus(OutboxStatus.PENDING.name());
        event.setAttempt(0);
        event.setMaxAttempts(properties.getMaxAttempts());
        event.setAvailableAt(now);
        event.setCreatedAt(now);
        event.setUpdatedAt(now);
        event.setVersion(0);

        int inserted = mapper.insertIdempotent(event);
        OutboxEvent persisted = event.getId() == null
                ? mapper.findByDeduplicationKey(event.getDeduplicationKey())
                : mapper.findById(event.getId());
        if (inserted == 1) afterCommit(() -> metrics.enqueued(event));
        return persisted == null ? event : persisted;
    }

    @Transactional
    public OutboxEvent claimNext(String dispatcherId) {
        LocalDateTime now = LocalDateTime.now();
        OutboxEvent candidate = mapper.lockNextPublishable(now);
        if (candidate == null) return null;

        String leaseToken = UUID.randomUUID().toString();
        LocalDateTime leaseExpiresAt = now.plusSeconds(Math.max(5, properties.getLeaseSeconds()));
        int updated = mapper.claim(candidate.getId(), candidate.getVersion(), dispatcherId,
                leaseToken, leaseExpiresAt, now);
        if (updated != 1) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Outbox event was claimed concurrently");
        }
        return mapper.findById(candidate.getId());
    }

    @Transactional
    public void markPublished(String eventId, String leaseToken) {
        LocalDateTime now = LocalDateTime.now();
        OutboxEvent event = requireActiveLease(eventId, leaseToken, now);
        int updated = mapper.markPublished(event.getId(), event.getVersion(), leaseToken, now);
        ensureOne(updated, "Outbox event changed while acknowledging publication");
        afterCommit(() -> metrics.published(event, now));
    }

    @Transactional
    public void markFailed(String eventId, String leaseToken, Throwable error) {
        LocalDateTime now = LocalDateTime.now();
        OutboxEvent event = requireActiveLease(eventId, leaseToken, now);
        String message = truncate(error == null ? "unknown publication failure" : error.toString());

        if (event.getAttempt() < event.getMaxAttempts()) {
            LocalDateTime availableAt = now.plusSeconds(retryDelaySeconds(event.getAttempt()));
            ensureOne(mapper.retry(event.getId(), event.getVersion(), leaseToken, availableAt, message, now),
                    "Outbox event changed while scheduling retry");
            afterCommit(() -> metrics.retried(event, "publish_failure"));
        } else {
            ensureOne(mapper.deadLetter(event.getId(), event.getVersion(), leaseToken, message, now),
                    "Outbox event changed while moving to DLQ");
            afterCommit(() -> metrics.deadLettered(event, "publish_failure"));
        }
    }

    @Transactional
    public int reclaimExpiredLeases() {
        LocalDateTime now = LocalDateTime.now();
        List<OutboxEvent> expired = mapper.lockExpiredLeases(now, properties.getReaperBatchSize());
        for (OutboxEvent event : expired) {
            String message = "Outbox dispatcher lease expired";
            if (event.getAttempt() < event.getMaxAttempts()) {
                ensureOne(mapper.recoverExpired(event.getId(), event.getVersion(), now, message, now),
                        "Expired Outbox event changed while recovering");
                afterCommit(() -> metrics.retried(event, "lease_expired"));
            } else {
                ensureOne(mapper.deadLetterExpired(event.getId(), event.getVersion(), message, now),
                        "Expired Outbox event changed while moving to DLQ");
                afterCommit(() -> metrics.deadLettered(event, "lease_expired"));
            }
        }
        return expired.size();
    }

    public List<OutboxEvent> listForUserAfter(String userId, long afterId, int limit) {
        int boundedLimit = Math.max(1, Math.min(limit, 200));
        return mapper.listForUserAfter(userId, Math.max(0, afterId), boundedLimit);
    }

    public JsonNode payload(OutboxEvent event) {
        try {
            return objectMapper.readTree(event.getPayloadJson());
        } catch (JsonProcessingException error) {
            throw new IllegalStateException("Stored Outbox payload is invalid JSON", error);
        }
    }

    int retryDelaySeconds(int attempt) {
        int exponent = Math.max(0, Math.min(attempt - 1, 10));
        long delay = (long) Math.max(1, properties.getRetryBaseSeconds()) * (1L << exponent);
        return (int) Math.min(delay, 3600L);
    }

    private Result<Object> withEventId(Result<?> notification, String eventId) {
        Map<String, Object> data = new LinkedHashMap<>();
        Object original = notification.getData();
        if (original instanceof Map) {
            for (Map.Entry<?, ?> entry : ((Map<?, ?>) original).entrySet()) {
                if (entry.getKey() != null) data.put(String.valueOf(entry.getKey()), entry.getValue());
            }
        } else if (original != null) {
            data.put("payload", original);
        }
        data.put("eventId", eventId);
        return new Result<>(notification.getCode(), notification.getMessage(), data);
    }

    private OutboxEvent requireActiveLease(String eventId, String leaseToken, LocalDateTime now) {
        OutboxEvent event = mapper.lockByEventId(eventId);
        boolean active = event != null && event.statusEnum() == OutboxStatus.PUBLISHING &&
                leaseToken != null && leaseToken.equals(event.getLeaseToken()) &&
                event.getLeaseExpiresAt() != null && event.getLeaseExpiresAt().isAfter(now);
        if (!active) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Outbox lease is missing or expired");
        }
        return event;
    }

    private String toJson(Object value) {
        try {
            return objectMapper.writeValueAsString(value);
        } catch (JsonProcessingException error) {
            throw new IllegalArgumentException("Outbox payload is not JSON serializable", error);
        }
    }

    private void ensureOne(int updated, String message) {
        if (updated != 1) throw new ResponseStatusException(HttpStatus.CONFLICT, message);
    }

    private String truncate(String value) {
        return value.length() <= MAX_ERROR_LENGTH ? value : value.substring(0, MAX_ERROR_LENGTH);
    }

    private void afterCommit(Runnable action) {
        if (TransactionSynchronizationManager.isActualTransactionActive() &&
                TransactionSynchronizationManager.isSynchronizationActive()) {
            TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
                @Override
                public void afterCommit() {
                    action.run();
                }
            });
            return;
        }
        action.run();
    }
}
