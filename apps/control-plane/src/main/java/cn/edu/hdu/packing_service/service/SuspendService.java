package cn.edu.hdu.packing_service.service;

import cn.edu.hdu.packing_service.pojo.Task;

public interface SuspendService {


    //增加任务
    Integer AddTask(String string, String orderID);

    //计算超时
    void TimeOut(Integer taskId);

    //计算接口
    void CalculateApi(String jsonData, Integer taskId);

    //更新任务结果
    void UpdateTask(int taskId, String result);

    //根据id查询任务
    Task findById(Integer taskId);



}
