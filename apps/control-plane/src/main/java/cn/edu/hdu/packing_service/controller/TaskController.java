package cn.edu.hdu.packing_service.controller;


import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.job.JobQueueService;
import cn.edu.hdu.packing_service.job.PackingJob;
import cn.edu.hdu.packing_service.job.dto.JobView;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;
import cn.edu.hdu.packing_service.service.SuspendService;
import cn.edu.hdu.packing_service.service.TaskService;
import cn.edu.hdu.packing_service.utils.DateUtil;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.parser.Feature;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/task")
public class TaskController {

    @Autowired
    private TaskService taskService;

    @Autowired
    private JobQueueService jobQueueService;

    @GetMapping("/list")
    public Result<PageBean<TaskDTO>> list(Integer pageNum,
                                          Integer pageSize,
                                          @RequestParam(required = false) String type,
                                          @RequestParam(required = false) String state,
                                          @RequestParam(required = false) String orderId,
                                          @RequestParam(required = false) String startTime,
                                          @RequestParam(required = false) String endTime
    ){
        PageBean<TaskDTO> res = taskService.list(pageNum, pageSize, type, state , orderId , startTime , endTime);
        return Result.success(res);
    }


    @DeleteMapping("/delete")
    public Result delete(Integer taskId) {
        //判断是否在计算中
        Task task = taskService.findById(taskId);

        //判断任务是否存在
        if (task == null) {
            return Result.error("任务不存在");
        }

        //判断字符中是否含有计算中
        if (task.getState().contains("计算中")) {
            return Result.error("当前任务计算中，无法删除");
        }
        //删除任务
        try {
            taskService.delete(task);
        } catch (IOException e) {
            Result.error("删除文件发生错误");
            e.printStackTrace();
        }

        return Result.success();
    }

    @PostMapping("/batch_delete")
    public Result batchDelete(@RequestBody List<Integer> taskIds) {
        //判断是否在计算中
        for (Integer taskId : taskIds) {
            Task task = taskService.findById(taskId);
            if (task.getState().equals("计算中")) {
                return Result.error("The task is being calculated and cannot be deleted.");
            }
        }
        //删除任务
        try {
            taskService.batchDelete(taskIds);
        } catch (IOException e) {
            Result.error("Failed to delete the task.");
            e.printStackTrace();
        }
        return Result.success();
    }

    @GetMapping("/detail")
    public Result detail(Integer taskId){
        //获取任务详情
        Task task = taskService.findById(taskId);

        //判断任务是否存在
        if (task == null) {
            return Result.error("任务不存在");
        }

        //判断是否已经计算完成
        if (task.getState().equals("计算中")) {
            return Result.error("The task is being calculated and cannot be viewed.");
        }

        //获取初始文件json
        String sourceJson = "";
        String resultJson = "";
        try {
            sourceJson = new String(Files.readAllBytes(Paths.get(task.getSourceJson())));
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            if (task.getResultJson() != null && !task.getResultJson().equals("")) {
                resultJson = new String(Files.readAllBytes(Paths.get(task.getResultJson())));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }


        JSONObject sourceJsonObj = JSONObject.parseObject(sourceJson, Feature.OrderedField);
        JSONObject resultJsonObj = JSONObject.parseObject(resultJson, Feature.OrderedField);
        System.out.println(DateUtil.getNowTime() + " 查询"+ taskId +"任务详情");
        JSONObject res = new JSONObject(true);
        res.put("sourceJson", sourceJsonObj);
        res.put("resultJson", resultJsonObj);
        res.put("task", task);
        return Result.success(res);



    }

    @GetMapping("/job")
    public Result<JobView> job(Integer taskId) {
        Task task = taskService.findById(taskId);
        if (task == null) return Result.error("任务不存在");

        Map<String, Object> claims = ThreadLocalUtil.get();
        Integer currentUser = (Integer) claims.get("id");
        if (!task.getCreateUser().equals(currentUser)) return Result.error("任务不存在");

        PackingJob job = jobQueueService.findLatestByTaskId(taskId);
        if (job == null) return Result.error("任务尚未进入计算队列");
        return Result.success(JobView.from(job));
    }



}
