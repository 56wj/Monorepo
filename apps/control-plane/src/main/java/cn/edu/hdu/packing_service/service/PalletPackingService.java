package cn.edu.hdu.packing_service.service;


import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;

import java.io.IOException;
import java.util.List;

public interface PalletPackingService {
    int i = 1;

    // 添加任务
    public Integer AddTask(String storagePath, String orderID);

    // 查询任务
    PageBean<TaskDTO> list(Integer pageNum, Integer pageSize, String type, String state ,String orderId , String startTime , String endTime);

    // 删除任务
    void delete(Task task) throws IOException;

    //根据id查询任务
    Task findById(Integer taskId);




    //第二次计算更新任务
    void secondUpdate(String storePath, Integer taskId);

}
