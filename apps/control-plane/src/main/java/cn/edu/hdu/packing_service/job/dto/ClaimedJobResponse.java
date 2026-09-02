package cn.edu.hdu.packing_service.job.dto;

import cn.edu.hdu.packing_service.job.PackingJob;
import com.fasterxml.jackson.databind.JsonNode;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class ClaimedJobResponse {
    private String jobId;
    private Integer taskId;
    private String jobType;
    private JsonNode payload;
    private Integer attempt;
    private Integer maxAttempts;
    private String leaseToken;
    private LocalDateTime leaseExpiresAt;

    public static ClaimedJobResponse from(PackingJob job, JsonNode payload) {
        return new ClaimedJobResponse(
                job.getPublicId(),
                job.getTaskId(),
                job.getJobType(),
                payload,
                job.getAttempt(),
                job.getMaxAttempts(),
                job.getLeaseToken(),
                job.getLeaseExpiresAt()
        );
    }
}
