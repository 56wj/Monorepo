package cn.edu.hdu.packing_service.controller;

import cn.edu.hdu.packing_service.job.PackingJobSubmissionService;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.service.PalletPackingService;
import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.service.TaskService;
import cn.edu.hdu.packing_service.utils.DateUtil;
import cn.edu.hdu.packing_service.utils.PalletPackingConfigValidator;
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
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/palletpacking")
public class PalletPackingController {

    @Autowired
    private PythonExecuteConfig pythonExecuteConfig; // python接口配置

    @Autowired
    private PalletPackingService palletPackingService;

    @Autowired
    private TaskService taskService;

    @Autowired
    private PackingJobSubmissionService jobSubmissionService;


    private final ObjectMapper objectMapper = new ObjectMapper();

    /*****
     * @Author: strelizia
     * @Date: 2024/3/5 10:50
     * @param: file
     * @return: Result
     * @Description: 一阶段计算任务
     */
    @PostMapping("/computer_first")
    public Result computerFirst(@RequestBody Map<String, Object> json) {
        System.out.println(DateUtil.getNowTime() + " - " + "获取到一阶段计算任务请求");
        if (!json.containsKey("data")) {
            return Result.error("The request doesn't contain a 'data' key.");
        }

        String configError = PalletPackingConfigValidator.validateRequest(json);
        if (configError != null) {
            return Result.error(configError);
        }

        // 获取orderID
        String orderID = (String) json.get("orderID");

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
        Integer taskId = jobSubmissionService.submitPalletFirst(sourcePath.toString(), orderID, data);

        return Result.success(taskId);
    }

    @PostMapping("/computer_second")
    public Result computerSecond(@RequestBody HashMap<String, Object> json) {
        System.out.println(DateUtil.getNowTime() + " - " + "获取到二阶段计算任务请求");
        if (!json.containsKey("data")) {
            return Result.error("The request doesn't contain a 'data' key.");
        }

        Object data = json.get("data");
        Integer taskId = (Integer) json.get("taskId");

        HashMap<String, Object> middleJsonData = new HashMap<>();
        middleJsonData.put("data", data);

        Path middleJosn = Paths.get(pythonExecuteConfig.getMiddle_save_path() + UUID.randomUUID() + ".json");

        if (Files.notExists(middleJosn.getParent())) {
            try {
                Files.createDirectories(middleJosn.getParent());
            } catch (IOException e) {
                e.printStackTrace();
                return Result.error("Failed to create directory.");
            }
        }


        String tmpJsonData = null;
        try {
            tmpJsonData = objectMapper.writeValueAsString(data);

            // 将JSON字符串写入文件
            Files.write(middleJosn, tmpJsonData.getBytes(StandardCharsets.UTF_8));

        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return Result.error("Failed to serialize 'data' to JSON.");
        } catch (IOException e) {
            e.printStackTrace();
            return Result.error("Failed to write JSON to file.");
        }

        //获取源文件
        Task task = palletPackingService.findById(taskId);

        String sourceJson = "";
        try {
            sourceJson = new String(Files.readAllBytes(Paths.get(task.getSourceJson())));
        } catch (IOException e) {
            e.printStackTrace();
            return Result.error("Failed to read the source file.");
        }

        JSONObject sourceJsonObj = JSONObject.parseObject(sourceJson, Feature.OrderedField);
        String configError = PalletPackingConfigValidator.validateData(sourceJsonObj);
        if (configError != null) {
            return Result.error(configError);
        }
        //将middleJsonData 转为JSONObject 格式
        JSONObject middleJsonObj = new JSONObject(middleJsonData);


        JSONObject res = new JSONObject(true);
        res.put("sourceJson", sourceJsonObj);
        res.put("middleJsonObj", middleJsonObj);
        res.put("taskId", taskId);

        //打印json数据
        //System.out.println(res);
        //更新任务状态
        jobSubmissionService.submitPalletSecond(taskId, middleJosn.toString(), res);

        return Result.success();
    }



    /***
     * @Author: strelizia
     * @Date: 2024/3/5 10:50
     * @return: Result
     * @Description:
     */
    @PostMapping("/test")
    public Result test(@RequestBody Map<String, Object> params) {
        System.out.println("params = " + params);
        // 直接返回接收到的params作为响应数据
        return Result.success(params);
    }

    //获取最新的任务
    @GetMapping("/getLatestTask")
    public Result getLatestTask() {
        Task task = taskService.getPalletLatestTask();

        if (task == null) {
            return Result.error("No Pallet Packing task found.");
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
