package cn.edu.hdu.packing_service.job;

import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.mapper.PalletPackingMapper;
import cn.edu.hdu.packing_service.mapper.SuspendMapper;
import cn.edu.hdu.packing_service.mapper.TaskMapper;
import cn.edu.hdu.packing_service.notification.TaskNotificationService;
import cn.edu.hdu.packing_service.pojo.Task;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.mockito.ArgumentCaptor;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

class JobResultHandlerTest {
    @TempDir Path directory;
    private final PalletPackingMapper pallet = mock(PalletPackingMapper.class);
    private final SuspendMapper suspend = mock(SuspendMapper.class);
    private final TaskMapper tasks = mock(TaskMapper.class);
    private final TaskNotificationService notifications = mock(TaskNotificationService.class);
    private final ObjectMapper json = new ObjectMapper();

    @Test
    void firstStagePersistsResultAndRegistersCommitHint() throws Exception {
        handler().handleSuccess(job(JobType.PALLET_FIRST), json.readTree("{\"result\":\"[]\"}"));
        verify(pallet).updateFirst(42, "[]");
        verify(notifications).notifyAfterCommit("9", 42);
    }

    @Test
    void secondStagePersistsFileAndRegistersCommitHint() throws Exception {
        handler().handleSuccess(job(JobType.PALLET_SECOND), json.readTree("{\"result\":{},\"resultExcel\":\"report.xlsx\"}"));
        ArgumentCaptor<String> path = ArgumentCaptor.forClass(String.class);
        verify(pallet).updateTask(eq(42), path.capture(), eq("report.xlsx"));
        assertEquals("{}", new String(Files.readAllBytes(Paths.get(path.getValue())), StandardCharsets.UTF_8));
        verify(notifications).notifyAfterCommit("9", 42);
    }

    @Test
    void suspendPersistsResultAndRegistersCommitHint() throws Exception {
        handler().handleSuccess(job(JobType.SUSPEND_FIRST), json.readTree("{\"result\":{}}"));
        verify(suspend).updateTask(eq(42), anyString());
        verify(notifications).notifyAfterCommit("9", 42);
    }

    @Test
    void terminalFailureUpdatesTaskAndRegistersCommitHint() {
        handler().handleTerminalFailure(job(JobType.PALLET_SECOND), "solver failed");
        verify(tasks).updateExecutionState(42, "计算失败");
        verify(notifications).notifyAfterCommit("9", 42);
    }

    @Test
    void invalidResultDoesNotNotify() throws Exception {
        JobResultHandler handler = handler();
        assertThrows(IllegalArgumentException.class, () -> handler.handleSuccess(job(JobType.PALLET_FIRST), json.readTree("{}")));
        verifyNoInteractions(notifications);
    }

    private JobResultHandler handler() {
        Task task = new Task(); task.setId(42); task.setCreateUser(9);
        when(tasks.findTaskById(42)).thenReturn(task);
        PythonExecuteConfig config = mock(PythonExecuteConfig.class);
        when(config.getResult_save_path()).thenReturn(directory.toString());
        return new JobResultHandler(pallet, suspend, tasks, config, notifications);
    }

    private PackingJob job(JobType type) {
        PackingJob job = new PackingJob(); job.setTaskId(42); job.setJobType(type.name());
        return job;
    }
}
