package cn.edu.hdu.packing_service.service.Impl;

import cn.edu.hdu.packing_service.mapper.PalletPackingMapper;
import cn.edu.hdu.packing_service.mapper.TaskMapper;
import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;
import cn.edu.hdu.packing_service.service.PalletPackingService;
import cn.edu.hdu.packing_service.stream.PalletPackingWebsocket;
import cn.edu.hdu.packing_service.utils.DateUtil;
import cn.edu.hdu.packing_service.utils.MyUtil;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import com.alibaba.fastjson.JSON;
import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import okhttp3.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;


@Service
public class PalletPackingServiceImp implements PalletPackingService {


    @Autowired
    private PythonExecuteConfig pythonExecuteConfig; // python接口配置

    @Autowired
    private PalletPackingMapper palletPackingMapper; // 数据库操作

    @Autowired
    private TaskMapper taskMapper; // 数据库操作

    /**
     * @Author: strelizia
     * @Date: 2024/1/30 11:54
     * @param: endpoint
     * @return: String
     * @Description: 调用python接口
     */
    @Override
    @Async
    public void FirstCalculateApi(String jsonData , Integer taskId) {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                MediaType JSON = MediaType.get("application/json; charset=utf-8");
                // 注意：这里需要根据实际情况调整JSON字符串的构造方式
                String jsonString = "{\"data\":" + jsonData + ",\"task_id\":\"" + taskId.toString() + "\"}";

                HttpUrl httpUrl = HttpUrl.parse(pythonExecuteConfig.getHost() + ":" + pythonExecuteConfig.getPort() + pythonExecuteConfig.getRoute() + "/pallet/first").newBuilder()
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



    public Integer AddTask(String storagePath, String orderID) {
        //获取当前用户
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer currentUser = (Integer) claims.get("id");

        Task task = new Task();
        //填充Task内容
        task.setSourceJson(storagePath);
        task.setOrderId(orderID);
        task.setType("托盘装箱");
        task.setState("一阶段计算中");
        task.setCreateUser(currentUser);
        task.setCreateTime(LocalDateTime.now());
        task.setUpdateTime(LocalDateTime.now());

        taskMapper.addTask(task);

        return task.getId();
    }


    @Override
    public void UpdateTask(Integer taskId, String jsonpath , String excelPath) {
        //获取任务
        Task task = taskMapper.findTaskById(taskId);
        //判断任务是否已经计算超时
        if (task.getState().equals("计算超时")){
            return;
        }else {
            //更新任务
            taskMapper.updateTask(taskId, jsonpath , excelPath);
        }
    }

    @Override
    public PageBean<TaskDTO> list(Integer pageNum, Integer pageSize, String type, String state , String orderId , String startTime , String endTime) {
        //创建PageBean对象
        PageBean<TaskDTO> res = new PageBean<>();

        //开启分页查询 PageHelper
        PageHelper.startPage(pageNum, pageSize);

        //获取用户id
        Map<String ,Object> claims = ThreadLocalUtil.get();
        Integer id = (Integer) claims.get("id");

        if (endTime != null && !endTime.equals("")){
            ZonedDateTime zonedDateTime = ZonedDateTime.parse(endTime);
            ZonedDateTime plusDays = zonedDateTime.plusDays(1);
            ZonedDateTime minusOneSecond = plusDays.minusSeconds(1);
            endTime = minusOneSecond.format(DateTimeFormatter.ISO_INSTANT);
        }

        //调用Mapper
        List<TaskDTO> taskList = taskMapper.list(id ,type , state,orderId , startTime , endTime);

        Page<TaskDTO> p = (Page<TaskDTO>) taskList;
        res.setTotal(p.getTotal());
        res.setItems(p.getResult());

        return res;
    }

    @Override
    public void delete(Task task) throws IOException {
        //获取文件路径
        String  source_path = task.getSourceJson();
        String  result_path = task.getResultJson();
        String  midlle_path = task.getMiddleJson();

        //删除result中的图片
        //获取任务id
        Integer taskId = task.getId();
        //构建图片地址
        Path imgPath = Paths.get(pythonExecuteConfig.getImage_path() + taskId.toString());
        System.out.println(imgPath);
        //删除文件夹
        if (Files.exists(imgPath)) {  // 确保路径存在
            try (Stream<Path> walk = Files.walk(imgPath)) {
                walk.sorted(Comparator.reverseOrder())  // 重要：需要反向排序，先删除文件，最后删除文件夹
                        .forEach(p -> {
                            try {
                                Files.delete(p);  // 删除每一个子路径
                            } catch (IOException e) {
                                System.err.println("Failed to delete " + p + " due to " + e.getMessage());
                            }
                        });
            }
        } else {
            System.out.println("File or Directory does not exist: " + imgPath);
        }

        //删除源文件
        if (source_path != null){
            if (Files.exists(Paths.get(source_path))){
                Files.delete(Paths.get(source_path));
            }
        }
        //删除结果文件
        if (result_path != null){
            if (Files.exists(Paths.get(result_path))){
                Files.delete(Paths.get(result_path));
            }
        }
        //删除中间文件
        if (midlle_path != null){
            if (Files.exists(Paths.get(midlle_path))){
                Files.delete(Paths.get(midlle_path));
            }
        }

        taskMapper.delete(task.getId());
    }


    @Async
    @Override
    public void timeOut(Integer taskId , Integer stage) {
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

                    //Todo
                    if (stage == 1 && task.getTagMiddle() != 1 && !task.getState().equals("网络错误")){
                        taskMapper.timeOut(taskId);
                        PalletPackingWebsocket.sendMessageByUserId(String.valueOf(userId), Result.error("小托计算超时"));
                    }

                    if (stage == 2 && !task.getState().equals("整托计算完成")&& !task.getState().equals("网络错误")) {
                        taskMapper.timeOut(taskId);
                        PalletPackingWebsocket.sendMessageByUserId(String.valueOf(userId), Result.error("整托计算超时"));
                    } else {
                        return;
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        };
        new Thread(runnable).start();
    }



    @Override
    public Task findById(Integer taskId) {
        return taskMapper.findTaskById(taskId);
    }



    @Override
    public void secondUpdate(String storePath, Integer taskId) {
        palletPackingMapper.secondUpdate(storePath, taskId);
    }

    @Async
    @Override
    public void SecondCalculateApi(String jsonData, Integer taskId) {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {

                // 构造JSON数据，这里假设jsonData是一个合法的JSON字符串，taskId是任务ID
                MediaType JSON = MediaType.get("application/json; charset=utf-8");
                // 注意：这里需要根据实际情况调整JSON字符串的构造方式

                HttpUrl httpUrl = HttpUrl.parse(pythonExecuteConfig.getHost() + ":" + pythonExecuteConfig.getPort() + pythonExecuteConfig.getRoute() + "/pallet/second").newBuilder()
                        .build();
                OkHttpClient client = new OkHttpClient(); // 创建okhttp客户端
                RequestBody body = RequestBody.create(jsonData, JSON); // 创建请求体
                Request request = new Request.Builder()// 创建POST请求
                        .url(httpUrl)
                        .post(body)
                        .build();
                try {
                    System.out.println(DateUtil.getNowTime() + "二阶段计算开始");
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
    public void UpdateFirst(int taskId, String result) {
        palletPackingMapper.updateFirst(taskId, result);
    }


}
