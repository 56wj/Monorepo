package cn.edu.hdu.packing_service.job;

import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.constant.StatusCodes;
import cn.edu.hdu.packing_service.mapper.PalletPackingMapper;
import cn.edu.hdu.packing_service.mapper.SuspendMapper;
import cn.edu.hdu.packing_service.mapper.TaskMapper;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.stream.PalletPackingWebsocket;
import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Component
public class JobResultHandler {
    private final PalletPackingMapper palletPackingMapper;
    private final SuspendMapper suspendMapper;
    private final TaskMapper taskMapper;
    private final PythonExecuteConfig pythonExecuteConfig;

    public JobResultHandler(PalletPackingMapper palletPackingMapper,
                            SuspendMapper suspendMapper,
                            TaskMapper taskMapper,
                            PythonExecuteConfig pythonExecuteConfig) {
        this.palletPackingMapper = palletPackingMapper;
        this.suspendMapper = suspendMapper;
        this.taskMapper = taskMapper;
        this.pythonExecuteConfig = pythonExecuteConfig;
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
                send(task, StatusCodes.PALLET_FIRST_CODE, "小托结果返回", result);
                break;
            case PALLET_SECOND:
                String palletResultPath = writeResultAtomically(result);
                String resultExcel = optionalText(output, "resultExcel");
                palletPackingMapper.updateTask(job.getTaskId(), palletResultPath, resultExcel);
                send(task, StatusCodes.PALLET_SECOND_CODE, "最终结果返回", result);
                break;
            case SUSPEND_FIRST:
                String suspendResultPath = writeResultAtomically(result);
                suspendMapper.updateTask(job.getTaskId(), suspendResultPath);
                send(task, StatusCodes.SUSPEND_FIRST_CODE, "悬空结果返回", result);
                break;
            default:
                throw new IllegalArgumentException("unsupported job type: " + job.getJobType());
        }
    }

    public void handleTerminalFailure(PackingJob job, String errorMessage) {
        taskMapper.updateExecutionState(job.getTaskId(), "计算失败");
        Task task = taskMapper.findTaskById(job.getTaskId());
        if (task != null) {
            PalletPackingWebsocket.sendMessageByUserId(
                    String.valueOf(task.getCreateUser()),
                    Result.error("计算失败: " + truncate(errorMessage, 160))
            );
        }
    }

    private void send(Task task, int code, String message, String result) {
        Map<String, Object> response = new HashMap<>();
        response.put("taskId", task.getId());
        response.put("result", result);
        PalletPackingWebsocket.sendMessageByUserId(
                String.valueOf(task.getCreateUser()),
                Result.success(code, message, response)
        );
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

    private String truncate(String value, int limit) {
        if (value == null) return "unknown error";
        return value.length() <= limit ? value : value.substring(0, limit);
    }
}
