package cn.edu.hdu.packing_service.job;

import cn.edu.hdu.packing_service.service.PalletPackingService;
import cn.edu.hdu.packing_service.service.SuspendService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;

@Service
public class PackingJobSubmissionService {
    private final JobQueueService jobQueueService;
    private final PalletPackingService palletPackingService;
    private final SuspendService suspendService;

    public PackingJobSubmissionService(JobQueueService jobQueueService,
                                       PalletPackingService palletPackingService,
                                       SuspendService suspendService) {
        this.jobQueueService = jobQueueService;
        this.palletPackingService = palletPackingService;
        this.suspendService = suspendService;
    }

    @Transactional
    public Integer submitPalletFirst(String sourcePath, String orderId, Object data) {
        Integer taskId = palletPackingService.AddTask(sourcePath, orderId);
        Map<String, Object> payload = new HashMap<>();
        payload.put("data", data);
        payload.put("task_id", String.valueOf(taskId));
        jobQueueService.enqueue(taskId, JobType.PALLET_FIRST, payload);
        return taskId;
    }

    @Transactional
    public void submitPalletSecond(Integer taskId, String middlePath, Object payload) {
        palletPackingService.secondUpdate(middlePath, taskId);
        jobQueueService.enqueue(taskId, JobType.PALLET_SECOND, payload);
    }

    @Transactional
    public Integer submitSuspendFirst(String sourcePath, String orderId, Object data) {
        Integer taskId = suspendService.AddTask(sourcePath, orderId);
        Map<String, Object> payload = new HashMap<>();
        payload.put("data", data);
        payload.put("taskId", String.valueOf(taskId));
        jobQueueService.enqueue(taskId, JobType.SUSPEND_FIRST, payload);
        return taskId;
    }
}
