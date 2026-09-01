package cn.edu.hdu.packing_service.service;


import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;

import java.io.IOException;
import java.util.List;

public interface PalletPackingService {
    int i = 1;

    // 调用python接口
    public void FirstCalculateApi(String jsonData , Integer taskId);

    // 添加任务
    public Integer AddTask(String storagePath, String orderID);

    // 更新任务
    void UpdateTask(Integer taskId, String jsonPath , String excelPath);

    // 查询任务
    PageBean<TaskDTO> list(Integer pageNum, Integer pageSize, String type, String state ,String orderId , String startTime , String endTime);

    // 删除任务
    void delete(Task task) throws IOException;

    //计算超时
    void timeOut(Integer taskId , Integer stage);

    //根据id查询任务
    Task findById(Integer taskId);




    //第二次计算更新任务
    void secondUpdate(String storePath, Integer taskId);

    //第二次计算调用python接口
    void SecondCalculateApi(String jsonData, Integer taskId);

    //第一次计算更新任务
    void UpdateFirst(int taskId, String result);
}
