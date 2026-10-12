package cn.edu.hdu.packing_service.job;

import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.mapper.PalletPackingMapper;
import cn.edu.hdu.packing_service.mapper.SuspendMapper;
import cn.edu.hdu.packing_service.mapper.TaskMapper;
import cn.edu.hdu.packing_service.notification.TaskNotificationService;
import cn.edu.hdu.packing_service.pojo.Task;
import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.UUID;

@Component
public class JobResultHandler {
    private final PalletPackingMapper palletPackingMapper;
    private final SuspendMapper suspendMapper;
    private final TaskMapper taskMapper;
    private final PythonExecuteConfig pythonExecuteConfig;
    private final TaskNotificationService notifications;

    public JobResultHandler(PalletPackingMapper palletPackingMapper,
                            SuspendMapper suspendMapper,
                            TaskMapper taskMapper,
                            PythonExecuteConfig pythonExecuteConfig,
                            TaskNotificationService notifications) {
        this.palletPackingMapper = palletPackingMapper;
        this.suspendMapper = suspendMapper;
        this.taskMapper = taskMapper;
        this.pythonExecuteConfig = pythonExecuteConfig;
        this.notifications = notifications;
    }

    public void handleSuccess(PackingJob job, JsonNode output) {
        Task task = taskMapper.findTaskById(job.getTaskId());
        if (task == null) {
            throw new IllegalStateException("legacy task does not exist: " + job.getTaskId());
        }

        String result = requiredText(output, "result");
        switch (job.typeEnum()) {
            case PALLET_FIRST:
                palletPackingMapper.updateFirst(job.getTaskId(), result);
                break;
            case PALLET_SECOND:
                String palletResultPath = writeResultAtomically(result);
                String resultExcel = optionalText(output, "resultExcel");
                palletPackingMapper.updateTask(job.getTaskId(), palletResultPath, resultExcel);
                break;
            case SUSPEND_FIRST:
                String suspendResultPath = writeResultAtomically(result);
                suspendMapper.updateTask(job.getTaskId(), suspendResultPath);
                break;
            default:
                throw new IllegalArgumentException("unsupported job type: " + job.getJobType());
        }
        notifications.notifyAfterCommit(String.valueOf(task.getCreateUser()), task.getId());
    }

    public void handleTerminalFailure(PackingJob job, String errorMessage) {
        taskMapper.updateExecutionState(job.getTaskId(), "计算失败");
        Task task = taskMapper.findTaskById(job.getTaskId());
        if (task != null) {
            notifications.notifyAfterCommit(String.valueOf(task.getCreateUser()), task.getId());
        }
    }

    private String writeResultAtomically(String result) {
        Path directory = Paths.get(pythonExecuteConfig.getResult_save_path());
        Path target = directory.resolve(UUID.randomUUID() + ".json");
        Path temporary = directory.resolve(target.getFileName() + ".tmp");
        try {
            Files.createDirectories(directory);
            Files.write(temporary, result.getBytes(StandardCharsets.UTF_8));
            try {
                Files.move(temporary, target, StandardCopyOption.ATOMIC_MOVE);
            } catch (IOException unsupportedAtomicMove) {
                Files.move(temporary, target, StandardCopyOption.REPLACE_EXISTING);
            }
            return target.toString();
        } catch (IOException error) {
            throw new IllegalStateException("failed to persist solver result", error);
        }
    }

    private String requiredText(JsonNode output, String field) {
        JsonNode value = output == null ? null : output.get(field);
        if (value == null || value.isNull()) {
            throw new IllegalArgumentException("solver output is missing '" + field + "'");
        }
        return value.isTextual() ? value.asText() : value.toString();
    }

    private String optionalText(JsonNode output, String field) {
        JsonNode value = output == null ? null : output.get(field);
        return value == null || value.isNull() ? null : value.asText();
    }

}
