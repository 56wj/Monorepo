package cn.edu.hdu.packing_service.job;

import cn.edu.hdu.packing_service.job.dto.ClaimJobRequest;
import cn.edu.hdu.packing_service.job.dto.ClaimedJobResponse;
import cn.edu.hdu.packing_service.job.dto.CompleteJobRequest;
import cn.edu.hdu.packing_service.job.dto.FailJobRequest;
import cn.edu.hdu.packing_service.job.dto.JobView;
import cn.edu.hdu.packing_service.job.dto.LeaseRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.Map;

@RestController
@RequestMapping("/internal/v1/jobs")
public class WorkerJobController {
    public static final String WORKER_TOKEN_HEADER = "X-Worker-Token";

    private final JobQueueService jobQueueService;
    private final WorkerTokenVerifier tokenVerifier;

    public WorkerJobController(JobQueueService jobQueueService, WorkerTokenVerifier tokenVerifier) {
        this.jobQueueService = jobQueueService;
        this.tokenVerifier = tokenVerifier;
    }

    @PostMapping("/claim")
    public ResponseEntity<ClaimedJobResponse> claim(
            @RequestHeader(value = WORKER_TOKEN_HEADER, required = false) String workerToken,
            @Valid @RequestBody ClaimJobRequest request) {
        tokenVerifier.verify(workerToken);
        PackingJob job = jobQueueService.claim(request);
        if (job == null) return ResponseEntity.noContent().build();
        return ResponseEntity.ok(ClaimedJobResponse.from(job, jobQueueService.payload(job)));
    }

    @PostMapping("/{jobId}/heartbeat")
    public ResponseEntity<Map<String, LocalDateTime>> heartbeat(
            @RequestHeader(value = WORKER_TOKEN_HEADER, required = false) String workerToken,
            @PathVariable String jobId,
            @Valid @RequestBody LeaseRequest request) {
        tokenVerifier.verify(workerToken);
        LocalDateTime leaseExpiresAt = jobQueueService.heartbeat(jobId, request.getLeaseToken());
        return ResponseEntity.ok(Collections.singletonMap("leaseExpiresAt", leaseExpiresAt));
    }

    @PostMapping("/{jobId}/complete")
    public ResponseEntity<Void> complete(
            @RequestHeader(value = WORKER_TOKEN_HEADER, required = false) String workerToken,
            @PathVariable String jobId,
            @Valid @RequestBody CompleteJobRequest request) {
        tokenVerifier.verify(workerToken);
        jobQueueService.complete(jobId, request.getLeaseToken(), request.getOutput());
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{jobId}/fail")
    public ResponseEntity<JobView> fail(
            @RequestHeader(value = WORKER_TOKEN_HEADER, required = false) String workerToken,
            @PathVariable String jobId,
            @Valid @RequestBody FailJobRequest request) {
        tokenVerifier.verify(workerToken);
        PackingJob job = jobQueueService.fail(jobId, request.getLeaseToken(), request.getErrorCode(),
                request.getErrorMessage(), request.isRetryable());
        return ResponseEntity.ok(JobView.from(job));
    }
}
