package cn.edu.hdu.packing_service.job;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ExpiredJobReaper {
    private final JobQueueService jobQueueService;

    public ExpiredJobReaper(JobQueueService jobQueueService) {
        this.jobQueueService = jobQueueService;
    }

    @Scheduled(fixedDelayString = "${job-queue.reaper-interval-ms:30000}")
    public void reclaimExpiredLeases() {
        jobQueueService.reclaimExpired();
    }
}
