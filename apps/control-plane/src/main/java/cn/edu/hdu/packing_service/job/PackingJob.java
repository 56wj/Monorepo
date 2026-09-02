package cn.edu.hdu.packing_service.job;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class PackingJob {
    private Long id;
    private String publicId;
    private String traceId;
    private Integer taskId;
    private String jobType;
    private String status;
    private String payloadJson;
    private String resultJson;
    private Integer priority;
    private Integer attempt;
    private Integer maxAttempts;
    private LocalDateTime availableAt;
    private String leaseOwner;
    private String leaseToken;
    private LocalDateTime leaseExpiresAt;
    private LocalDateTime heartbeatAt;
    private String idempotencyKey;
    private String errorCode;
    private String errorMessage;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime startedAt;
    private LocalDateTime finishedAt;
    private Integer version;

    public JobStatus statusEnum() {
        return JobStatus.valueOf(status);
    }

    public JobType typeEnum() {
        return JobType.valueOf(jobType);
    }
}
