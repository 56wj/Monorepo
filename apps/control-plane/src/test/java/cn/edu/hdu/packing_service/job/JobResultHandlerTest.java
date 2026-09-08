package cn.edu.hdu.packing_service.job;

import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.mapper.PalletPackingMapper;
import cn.edu.hdu.packing_service.mapper.SuspendMapper;
import cn.edu.hdu.packing_service.mapper.TaskMapper;
import cn.edu.hdu.packing_service.outbox.OutboxService;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.pojo.Task;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class JobResultHandlerTest {

    @Test
    void successfulBusinessUpdateEnqueuesDurableEventInsteadOfSendingInline() throws Exception {
        PalletPackingMapper palletMapper = mock(PalletPackingMapper.class);
        SuspendMapper suspendMapper = mock(SuspendMapper.class);
        TaskMapper taskMapper = mock(TaskMapper.class);
        OutboxService outboxService = mock(OutboxService.class);
        Task task = task();
        when(taskMapper.findTaskById(42)).thenReturn(task);
        JobResultHandler handler = new JobResultHandler(palletMapper, suspendMapper, taskMapper,
                mock(PythonExecuteConfig.class), outboxService);
        PackingJob job = job(JobType.PALLET_FIRST);

        handler.handleSuccess(job, new ObjectMapper().readTree("{\"result\":\"{\\\"ok\\\":true}\"}"));

        verify(palletMapper).updateFirst(42, "{\"ok\":true}");
        ArgumentCaptor<Result> notification = ArgumentCaptor.forClass(Result.class);
        verify(outboxService).enqueueTaskEvent(eq(job), eq("9"),
                eq("PALLET_FIRST_COMPLETED"), notification.capture());
        Map<?, ?> data = (Map<?, ?>) notification.getValue().getData();
        assertEquals(42, data.get("taskId"));
        assertEquals("{\"ok\":true}", data.get("result"));
    }

    @Test
    void terminalFailureUpdatesTaskAndEnqueuesDurableFailureEvent() {
        PalletPackingMapper palletMapper = mock(PalletPackingMapper.class);
        SuspendMapper suspendMapper = mock(SuspendMapper.class);
        TaskMapper taskMapper = mock(TaskMapper.class);
        OutboxService outboxService = mock(OutboxService.class);
        when(taskMapper.findTaskById(42)).thenReturn(task());
        JobResultHandler handler = new JobResultHandler(palletMapper, suspendMapper, taskMapper,
                mock(PythonExecuteConfig.class), outboxService);
        PackingJob job = job(JobType.PALLET_SECOND);

        handler.handleTerminalFailure(job, "solver failed");

        verify(taskMapper).updateExecutionState(42, "计算失败");
        verify(outboxService).enqueueTaskEvent(eq(job), eq("9"),
                eq("PACKING_JOB_FAILED"), any(Result.class));
    }

    private PackingJob job(JobType type) {
        PackingJob job = new PackingJob();
        job.setPublicId("job-public-1");
        job.setTraceId("trace-12345678");
        job.setTaskId(42);
        job.setJobType(type.name());
        return job;
    }

    private Task task() {
        Task task = new Task();
        task.setId(42);
        task.setCreateUser(9);
        return task;
    }
}
