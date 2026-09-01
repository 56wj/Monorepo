package cn.edu.hdu.packing_service.service.Impl;

import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.mapper.PalletPackingMapper;
import cn.edu.hdu.packing_service.mapper.SuspendMapper;
import cn.edu.hdu.packing_service.mapper.TaskMapper;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.service.SuspendService;
import cn.edu.hdu.packing_service.stream.PalletPackingWebsocket;
import cn.edu.hdu.packing_service.utils.DateUtil;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import okhttp3.*;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Map;

@Service
public class SuspendServiceImpl implements SuspendService {

    @Autowired
    private PythonExecuteConfig pythonExecuteConfig; // python接口配置

    @Autowired
    private SuspendMapper suspendMapper; // 数据库操作

    @Autowired
    private TaskMapper taskMapper; // 数据库操作

    @Override
    public Integer AddTask(String savePath, String orderID) {
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer currentUserId = (Integer) claims.get("id");

        Task task = new Task();
        task.setSourceJson(savePath);
        task.setOrderId(orderID);
        task.setType("悬空装箱");
        task.setState("一阶段计算中");
        task.setCreateUser(currentUserId);
        task.setCreateTime(LocalDateTime.now());
        task.setUpdateTime(LocalDateTime.now());

        taskMapper.addTask(task);
        return task.getId();
    }

    @Override
    public void TimeOut(Integer taskId) {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(1000 * 60 * 20); // 20分钟
                    Task task = taskMapper.findTaskById(taskId);

                    //获取用户id
                    Integer userId = taskMapper.findTaskById(taskId).getCreateUser();
                    if (task == null){
                        return;
                    }

                    if (!task.getState().equals("悬空计算完成")&& !task.getState().equals("网络错误")) {
                        taskMapper.timeOut(taskId);
                        System.out.println(DateUtil.getNowTime() + " 悬空计算超时");
                        // Todo
                        PalletPackingWebsocket.sendMessageByUserId(String.valueOf(userId), Result.error("计算超时"));
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        };
        new Thread(runnable).start();
    }

    @Override
    public void CalculateApi(String jsonData, Integer taskId) {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                MediaType JSON = MediaType.get("application/json; charset=utf-8");
                // 注意：这里需要根据实际情况调整JSON字符串的构造方式
                String jsonString = "{\"data\":" + jsonData + ",\"taskId\":\"" + taskId.toString() + "\"}";
                System.out.println(jsonString);
                HttpUrl httpUrl = HttpUrl.parse(pythonExecuteConfig.getHost() + ":" + pythonExecuteConfig.getPort() + pythonExecuteConfig.getRoute() + "/suspend/first").newBuilder()
                        .build();

                OkHttpClient client = new OkHttpClient(); // 创建okhttp客户端
                RequestBody body = RequestBody.create(jsonString, JSON); // 创建请求体
                Request request = new Request.Builder()// 创建POST请求
                        .url(httpUrl)
                        .post(body)
                        .build();
                try {
                    System.out.println(DateUtil.getNowTime() + " 一阶段开始计算");
                    client.newCall(request).execute().body().string(); // 获取python接口返回的数据
                }catch (Exception e){
                    e.printStackTrace();
                    //非超时错误
                    if (!e.getMessage().equals("timeout")) {
                        taskMapper.connectError(taskId);
                    }
                }
            }
        };
        new Thread(runnable).start();
    }

    @Override
    public void UpdateTask(int taskId, String jsonpath) {
        //获取任务
        Task task = taskMapper.findTaskById(taskId);

        if (task.getState().equals("计算超时")){
            return;
        }else {
            //更新任务
            suspendMapper.updateTask(taskId, jsonpath);
        }
    }

    @Override
    public Task findById(Integer taskId) {
        return taskMapper.findTaskById(taskId);
    }



}
