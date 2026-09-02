package cn.edu.hdu.packing_service.job.dto;

import cn.edu.hdu.packing_service.job.PackingJob;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class JobView {
    private String jobId;
    private String traceId;
    private Integer taskId;
    private String jobType;
    private String status;
    private Integer attempt;
    private Integer maxAttempts;
    private String errorCode;
    private String errorMessage;
    private LocalDateTime createdAt;
    private LocalDateTime startedAt;
    private LocalDateTime finishedAt;

    public static JobView from(PackingJob job) {
        return new JobView(job.getPublicId(), job.getTraceId(), job.getTaskId(), job.getJobType(), job.getStatus(),
                job.getAttempt(), job.getMaxAttempts(), job.getErrorCode(), job.getErrorMessage(),
                job.getCreatedAt(), job.getStartedAt(), job.getFinishedAt());
    }
}
