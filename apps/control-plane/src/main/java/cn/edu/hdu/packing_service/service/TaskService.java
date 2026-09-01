package cn.edu.hdu.packing_service.service;

import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;

import java.io.IOException;
import java.util.List;

public interface TaskService {


    public PageBean<TaskDTO> list(Integer pageNum, Integer pageSize, String type, String state , String orderId , String startTime , String endTime);

    //根据id查询任务
    Task findById(Integer taskId);

    // 删除任务
    void delete(Task task) throws IOException;

    //批量删除
    void batchDelete(List<Integer> taskIds) throws IOException;

    //获取托盘装箱最新任务
    Task getPalletLatestTask();

    //获取悬空装箱最新任务
    Task getSuspandLatestTask();
}
