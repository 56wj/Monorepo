package cn.edu.hdu.packing_service.service.Impl;

import cn.edu.hdu.packing_service.mapper.TaskMapper;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.service.SuspendService;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Map;

@Service
public class SuspendServiceImpl implements SuspendService {

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

}
