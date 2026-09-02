package cn.edu.hdu.packing_service.job;

import cn.edu.hdu.packing_service.job.dto.ClaimJobRequest;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class JobQueueService {
    private final PackingJobMapper mapper;
    private final JobQueueProperties properties;
    private final JobResultHandler resultHandler;
    private final ObjectMapper objectMapper;

    public JobQueueService(PackingJobMapper mapper,
                           JobQueueProperties properties,
                           JobResultHandler resultHandler,
                           ObjectMapper objectMapper) {
        this.mapper = mapper;
        this.properties = properties;
        this.resultHandler = resultHandler;
        this.objectMapper = objectMapper;
    }

    @Transactional
    public PackingJob enqueue(Integer taskId, JobType jobType, Object payload) {
        LocalDateTime now = LocalDateTime.now();
        PackingJob job = new PackingJob();
        job.setPublicId(UUID.randomUUID().toString());
        job.setTaskId(taskId);
        job.setJobType(jobType.name());
        job.setStatus(JobStatus.QUEUED.name());
        job.setPayloadJson(toJson(payload));
        job.setPriority(0);
        job.setAttempt(0);
        job.setMaxAttempts(properties.getMaxAttempts());
        job.setAvailableAt(now);
        job.setIdempotencyKey("task:" + taskId + ":" + jobType.name());
        job.setCreatedAt(now);
        job.setUpdatedAt(now);
        job.setVersion(0);
        mapper.insertIdempotent(job);
        return mapper.findById(job.getId());
    }

    @Transactional
    public PackingJob claim(ClaimJobRequest request) {
        LocalDateTime now = LocalDateTime.now();
        reclaimExpiredLocked(now);

        List<String> capabilities = validatedCapabilities(request.getCapabilities());
        PackingJob candidate = mapper.lockNextClaimable(capabilities, now);
        if (candidate == null) return null;

        JobStatus from = candidate.statusEnum();
        requireTransition(from, JobStatus.RUNNING);
        int leaseSeconds = clampLeaseSeconds(request.getLeaseSeconds());
        String leaseToken = UUID.randomUUID().toString();
        LocalDateTime leaseExpiresAt = now.plusSeconds(leaseSeconds);
        int updated = mapper.claim(candidate.getId(), candidate.getVersion(), request.getWorkerId(),
                leaseToken, leaseExpiresAt, now);
        if (updated != 1) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "job was claimed concurrently");
        }
        return mapper.findById(candidate.getId());
    }

    @Transactional
    public LocalDateTime heartbeat(String publicId, String leaseToken) {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime expiresAt = now.plusSeconds(properties.getDefaultLeaseSeconds());
        int updated = mapper.heartbeat(publicId, leaseToken, expiresAt, now);
        if (updated != 1) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "job lease is missing or expired");
        }
        return expiresAt;
    }

    @Transactional
    public void complete(String publicId, String leaseToken, JsonNode output) {
        LocalDateTime now = LocalDateTime.now();
        PackingJob job = mapper.lockByPublicId(publicId);
        if (job != null && job.statusEnum() == JobStatus.SUCCEEDED) {
            return;
        }
        validateActiveLease(job, leaseToken, now);
        requireTransition(JobStatus.RUNNING, JobStatus.SUCCEEDED);
        resultHandler.handleSuccess(job, output);
        int updated = mapper.succeed(job.getId(), job.getVersion(), leaseToken, toJson(output), now);
        if (updated != 1) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "job changed while completing");
        }
    }

    @Transactional
    public PackingJob fail(String publicId,
                           String leaseToken,
                           String errorCode,
                           String errorMessage,
                           boolean retryable) {
        LocalDateTime now = LocalDateTime.now();
        PackingJob job = requireActiveLease(publicId, leaseToken, now);
        String normalizedCode = truncate(errorCode == null ? "SOLVER_ERROR" : errorCode, 64);
        String normalizedMessage = truncate(errorMessage == null ? "solver failed" : errorMessage, 1000);

        if (retryable && job.getAttempt() < job.getMaxAttempts()) {
            requireTransition(JobStatus.RUNNING, JobStatus.RETRY_WAIT);
            LocalDateTime availableAt = now.plusSeconds(retryDelaySeconds(job.getAttempt()));
            ensureOne(mapper.retry(job.getId(), job.getVersion(), availableAt,
                    normalizedCode, normalizedMessage, now));
        } else {
            requireTransition(JobStatus.RUNNING, JobStatus.DEAD_LETTER);
            ensureOne(mapper.deadLetter(job.getId(), job.getVersion(),
                    normalizedCode, normalizedMessage, now));
            resultHandler.handleTerminalFailure(job, normalizedMessage);
        }
        return mapper.findById(job.getId());
    }

    @Transactional
    public int reclaimExpired() {
        return reclaimExpiredLocked(LocalDateTime.now());
    }

    public PackingJob findByPublicId(String publicId) {
        return mapper.findByPublicId(publicId);
    }

    public PackingJob findLatestByTaskId(Integer taskId) {
        return mapper.findLatestByTaskId(taskId);
    }

    public JsonNode payload(PackingJob job) {
        try {
            return objectMapper.readTree(job.getPayloadJson());
        } catch (JsonProcessingException error) {
            throw new IllegalStateException("stored job payload is invalid JSON", error);
        }
    }

    int retryDelaySeconds(int attempt) {
        int exponent = Math.max(0, Math.min(attempt - 1, 10));
        long delay = (long) properties.getRetryBaseSeconds() * (1L << exponent);
        return (int) Math.min(delay, 3600L);
    }

    private int reclaimExpiredLocked(LocalDateTime now) {
        List<PackingJob> expired = mapper.lockExpiredLeases(now, properties.getReaperBatchSize());
        for (PackingJob job : expired) {
            if (job.getAttempt() < job.getMaxAttempts()) {
                requireTransition(JobStatus.RUNNING, JobStatus.RETRY_WAIT);
                ensureOne(mapper.retry(job.getId(), job.getVersion(), now, "LEASE_EXPIRED",
                        "worker heartbeat expired", now));
            } else {
                requireTransition(JobStatus.RUNNING, JobStatus.DEAD_LETTER);
                ensureOne(mapper.deadLetter(job.getId(), job.getVersion(), "LEASE_EXPIRED",
                        "worker heartbeat expired after maximum attempts", now));
                resultHandler.handleTerminalFailure(job, "worker heartbeat expired after maximum attempts");
            }
        }
        return expired.size();
    }

    private PackingJob requireActiveLease(String publicId, String leaseToken, LocalDateTime now) {
        PackingJob job = mapper.lockByPublicId(publicId);
        validateActiveLease(job, leaseToken, now);
        return job;
    }

    private void validateActiveLease(PackingJob job, String leaseToken, LocalDateTime now) {
        boolean active = job != null && job.statusEnum() == JobStatus.RUNNING &&
                leaseToken != null && leaseToken.equals(job.getLeaseToken()) &&
                job.getLeaseExpiresAt() != null && job.getLeaseExpiresAt().isAfter(now);
        if (!active) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "job lease is missing or expired");
        }
    }

    private List<String> validatedCapabilities(List<String> rawCapabilities) {
        List<String> capabilities = new ArrayList<>();
        try {
            for (String raw : rawCapabilities) {
                capabilities.add(JobType.valueOf(raw).name());
            }
        } catch (IllegalArgumentException error) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "unknown worker capability");
        }
        return capabilities;
    }

    private int clampLeaseSeconds(Integer requested) {
        int value = requested == null ? properties.getDefaultLeaseSeconds() : requested;
        return Math.max(10, Math.min(value, properties.getMaxLeaseSeconds()));
    }

    private void requireTransition(JobStatus from, JobStatus to) {
        if (!from.canTransitionTo(to)) {
            throw new IllegalStateException("invalid job transition: " + from + " -> " + to);
        }
    }

    private void ensureOne(int updated) {
        if (updated != 1) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "job changed concurrently");
        }
    }

    private String toJson(Object value) {
        try {
            return objectMapper.writeValueAsString(value);
        } catch (JsonProcessingException error) {
            throw new IllegalArgumentException("job data is not JSON serializable", error);
        }
    }

    private String truncate(String value, int limit) {
        return value.length() <= limit ? value : value.substring(0, limit);
    }
}
