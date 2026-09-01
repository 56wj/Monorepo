package cn.edu.hdu.packing_service.controller;

import cn.edu.hdu.packing_service.constant.StatusCodes;
import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;
import cn.edu.hdu.packing_service.service.PalletPackingService;
import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.service.TaskService;
import cn.edu.hdu.packing_service.stream.PalletPackingWebsocket;
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
import java.util.List;
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
        Integer taskId = palletPackingService.AddTask(sourcePath.toString() , orderID);

        palletPackingService.timeOut(taskId, 1);

        //打印json数据
        //System.out.println(jsonData);

        palletPackingService.FirstCalculateApi(jsonData , taskId);

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
        palletPackingService.secondUpdate(middleJosn.toString() , taskId);

        //启动计时器
        System.out.println(DateUtil.getNowTime() + " - " + "启动计时器");
        palletPackingService.timeOut(taskId,2);

        //开始第二次计算
        System.out.println(DateUtil.getNowTime() + " - " + "开始第二次计算");
        palletPackingService.SecondCalculateApi(res.toJSONString() , taskId);

        return Result.success();
    }



    @PostMapping("/resultback_first")
    public Result resultbackFirst(@RequestBody Map<String, Object> data) {
        System.out.println(DateUtil.getNowTime() + " - " + "获取到一阶段计算结果反馈请求");

        if (!data.containsKey("taskId") || !data.containsKey("result")) {
            return Result.error("The request doesn't contain a 'taskId' or 'result' key.");
        }

        //获取任务id
        int taskId = Integer.parseInt((String) data.get("taskId"));

        //打印结果
//        System.out.println(data.get("result"));

        //获取结果
        String result = (String) data.get("result");

        //更新任务状态
        palletPackingService.UpdateFirst(taskId , result);

        //获取当前用户
        Task task = palletPackingService.findById(taskId);

        //判断任务是否存在
        if(task == null){
            return Result.error("The task doesn't exist.");
        }
        Integer currentUser = task.getCreateUser();


        //封装返回结果
        Map<String , Object> res = new HashMap<>();
        res.put("taskId" , taskId);
        res.put("result" , result);

        //发送websocket
        System.out.println(DateUtil.getNowTime() + " - " + "一阶段结果返回");
        PalletPackingWebsocket.sendMessageByUserId(String.valueOf(currentUser), Result.success(StatusCodes.PALLET_FIRST_CODE ,"小托结果返回", res));

        return Result.success();


    }

    /***
     * @Author: strelizia
     * @Date: 2024/3/9 19:23
     * @param: taskId
     * @param: result
     * @return: Result
     * @Description:
     */
    @PostMapping("/resultback_second")
    public Result resultbackSecond(@RequestBody Map<String, Object> data) {
        System.out.println(DateUtil.getNowTime() + " - " + "获取到二阶段计算结果反馈请求");
        if (!data.containsKey("taskId") || !data.containsKey("result")) {
            return Result.error("The request doesn't contain a 'taskId' or 'result' key.");
        }

        //获取任务id
        int taskId = (Integer) data.get("taskId");

        //获取结果
        String result = (String) data.get("result");

        //获取结果excel路径
        String excelPath = (String) data.get("resultExcel");


        Path resultPath = Paths.get(pythonExecuteConfig.getResult_save_path() + UUID.randomUUID() + ".json");

        //判断是否存在该文件夹
        if(Files.notExists(resultPath.getParent())){
            try {
                Files.createDirectories(resultPath.getParent());
            } catch (IOException e) {
                e.printStackTrace();
                return Result.error("Failed to create directory.");
            }
        }

        //将结果写入文件
        try {
            Files.write(resultPath, result.getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println(DateUtil.getNowTime() + " - " + "二阶段结果写入文件");


        //获取当前用户
        Task task = palletPackingService.findById(taskId);

        //判断任务是否存在
        if(task == null){
            return Result.error("任务不存在");
        }

        Integer currentUser = task.getCreateUser();

        //更新任务状态
        palletPackingService.UpdateTask(taskId , resultPath.toString() , excelPath);

        Map<String , Object> res = new HashMap<>();
        res.put("taskId" , taskId);
        res.put("result" , result);

        //发送websocket
        System.out.println(DateUtil.getNowTime() + " - " + "二阶段结果返回");
        PalletPackingWebsocket.sendMessageByUserId(String.valueOf(currentUser), Result.success(StatusCodes.PALLET_SECOND_CODE ,"最终结果返回", res));

        return Result.success("websocket已发送");
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
