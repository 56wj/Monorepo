package cn.edu.hdu.packing_service.controller;


import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.job.PackingJobSubmissionService;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.service.SuspendService;
import cn.edu.hdu.packing_service.service.TaskService;
import cn.edu.hdu.packing_service.utils.DateUtil;
import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.parser.Feature;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/suspend")
public class SuspendController {

    @Autowired
    private PythonExecuteConfig pythonExecuteConfig; // python接口配置

    @Autowired
    private SuspendService suspendService;

    @Autowired
    private TaskService taskService;

    @Autowired
    private PackingJobSubmissionService jobSubmissionService;

    private final ObjectMapper objectMapper = new ObjectMapper();




    @PostMapping("/computer_first")
    public Result computerFirst(@RequestBody Map<String,Object> json) {
        System.out.println(DateUtil.getNowTime() + " - " + "获取到悬空装箱请求");

        //时区转化
        HashMap<String , Object> data1 = (HashMap<String, Object>) json.get("data");
        HashMap<String , Object> config = (HashMap<String, Object>) data1.get("config");

        String utcTimeString = (String) config.get("recDate");

        //判断是否为世界时间
        if (utcTimeString.endsWith("Z")) {

            Instant instant = Instant.parse(utcTimeString);

            // 转换为北京时间
            ZonedDateTime beijingTime = instant.atZone(ZoneId.of("Asia/Shanghai"));

            // 格式化输出
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
            String recDate = beijingTime.format(formatter);

            //修改时间
            config.put("recDate", recDate);
            //修改回去
            data1.put("config", config);
            json.put("data", data1);
        }
        
        if (!json.containsKey("data")){
            return Result.error("请求需要包含data数据");
        }

        if (!json.containsKey("orderID")){
            return Result.error("请求需要包含orderID数据");
        }

        String orderID = json.get("orderID").toString();

        Object data = json.get("data");

        Path sourcePath = Paths.get(pythonExecuteConfig.getSource_save_path() + UUID.randomUUID() + ".json");

        if(Files.notExists(sourcePath.getParent())){
            try {
                Files.createDirectories(sourcePath.getParent());
            } catch (IOException e) {
                e.printStackTrace();
                return Result.error("Failed to create directory.");
            }
        }

        String jsonData = null;
        try {
            jsonData = objectMapper.writeValueAsString(data);

            // 将JSON字符串写入文件
            Files.write(sourcePath, jsonData.getBytes(StandardCharsets.UTF_8));

        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return Result.error("Failed to serialize 'data' to JSON.");
        } catch (IOException e) {
            e.printStackTrace();
            return Result.error("Failed to write JSON to file.");
        }

        Integer taskId = jobSubmissionService.submitSuspendFirst(sourcePath.toString(), orderID, data);

        return Result.success(taskId);
    }


    @GetMapping("/getLatestTask")
    public Result getLatestTask() {
        Task task = taskService.getSuspandLatestTask();

        if (task == null) {
            return Result.error("No Suspend Packing task found.");
        }
        //获取初始文件json
        String sourceJson = "";
        String resultJson = "";
        try {
            sourceJson = new String(Files.readAllBytes(Paths.get(task.getSourceJson())));
            resultJson = new String(Files.readAllBytes(Paths.get(task.getResultJson())));
        } catch (IOException e) {
            e.printStackTrace();
            return Result.error("Failed to read the source file.");
        }
        //返回任务详情
        JSONObject sourceJsonObj = JSONObject.parseObject(sourceJson, Feature.OrderedField);
        JSONObject resultJsonObj = JSONObject.parseObject(resultJson, Feature.OrderedField);


        JSONObject res = new JSONObject(true);
        res.put("sourceJson", sourceJsonObj);
        res.put("resultJson", resultJsonObj);
        res.put("task", task);

        return Result.success(res);
    }


}
