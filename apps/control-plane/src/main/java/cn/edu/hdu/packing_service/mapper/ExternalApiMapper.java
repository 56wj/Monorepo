package cn.edu.hdu.packing_service.mapper;

import cn.edu.hdu.packing_service.pojo.PushTask;
import org.apache.ibatis.annotations.*;

@Mapper
public interface ExternalApiMapper {

    // 该方法用于记录三方系统发送任务
    @Options(useGeneratedKeys = true, keyProperty = "pid", keyColumn = "pid")
    @Insert("insert into push_task (order_id, type, order_data, read_status, push_time) values (#{orderId}, #{type}, #{orderData}, #{readStatus}, #{pushTime})")
    Integer addTask(PushTask pushTask);

    // 该方法用于获取三方系统发送的任务
    @Select("select * from push_task where pid = #{pushId}")
    PushTask getTask(Integer pushId);

    @Update("update push_task set read_status = 1 where pid = #{pushId}")
    void updateTaskStatus(Integer pushId);
}
