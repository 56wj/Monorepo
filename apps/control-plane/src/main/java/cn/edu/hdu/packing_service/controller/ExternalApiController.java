package cn.edu.hdu.packing_service.controller;


import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.constant.StatusCodes;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.service.ExternalApiService;
import cn.edu.hdu.packing_service.utils.DateUtil;
import com.alibaba.fastjson.JSONObject;
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
@RequestMapping("/externalApi")
public class ExternalApiController {

    @Autowired
    private PythonExecuteConfig pythonExecuteConfig; // python接口配置

    @Autowired
    private ExternalApiService externalApiService;

    private final ObjectMapper objectMapper = new ObjectMapper(); // JSON序列化工具

    @PostMapping("/stock/push_data")
    public Result pushData(@RequestBody Map<String, Object> json) {
        System.out.println(DateUtil.getNowTime() + " - " + "获取库存平台推送数据");

        //判断是否存在data字段
        if (!json.containsKey("orderData")) {
            return Result.error("The request doesn't contain a 'data' key.");
        }

        //判断是否存在type字段
        if (!json.containsKey("type")) {
            return Result.error("The request doesn't contain a 'type' key.");
        }

        //判断orderId是否存在
        if (!json.containsKey("orderId")) {
            return Result.error("The request doesn't contain a 'orderId' key.");
        }

        //获取orderId
        String orderID = (String) json.get("orderId");

        //获取type
        String type = (String) json.get("type");

        //序列化数据
        //转化为Map格式
        Map<String, Object> dataMap = new HashMap<>();
        dataMap.put("tableData" , json.get("orderData"));

        String jsonData = null;
        try {
            jsonData = objectMapper.writeValueAsString(dataMap);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return Result.error("Failed to serialize 'data' to JSON.");
        }

        Path pushPath = Paths.get(pythonExecuteConfig.getPush_save_path() + UUID.randomUUID() + ".json");

        //判断文件位置是否存在
        if (!pushPath.toFile().exists()) {
            try {
                Files.createDirectories(pushPath.getParent());
            } catch (IOException e) {
                e.printStackTrace();
                return Result.error("Failed to create directory.");
            }
        }

        //将数据写入文件
        try {
            // 将JSON字符串写入文件
            Files.write(pushPath, jsonData.getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            e.printStackTrace();
            return Result.error("Failed to write JSON to file.");
        }

        System.out.println(DateUtil.getNowTime() + " - " + orderID + "订单推送数据写入文件成功");

        //任务写入mysql
        Integer push_id =  externalApiService.addTask(orderID, type, pushPath.toString());

        System.out.println(DateUtil.getNowTime() + " - " + orderID + "订单推送任务写入数据库成功");
        return Result.success(0 , "Order push successful", push_id);
    }


    //查询推送任务
    @GetMapping("/stock/get_push_task")
    public Result getPushTask(Integer pushId) {
        System.out.println(DateUtil.getNowTime() + " - " + pushId + "获取库存平台推送任务");

        //判断是否存在pushId字段
        if (pushId == null) {
            return Result.error("The request doesn't contain a 'pushId' key.");
        }

        //查询任务
        JSONObject task = externalApiService.getTask(pushId);

        //判断任务是否存在
        if (task.containsKey("error")) {
            if (task.getInteger("error") == StatusCodes.TASK_NULL_ERROR) {
                return Result.error("The task does not exist.");
            } else if (task.getInteger("error") == StatusCodes.FILE_READ_ERROR) {
                return Result.error("Failed to read file.");
            }
        }

        return Result.success(task);
    }

}
