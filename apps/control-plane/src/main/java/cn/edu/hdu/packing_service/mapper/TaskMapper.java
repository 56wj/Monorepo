package cn.edu.hdu.packing_service.mapper;

import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface TaskMapper {


    @Options(useGeneratedKeys = true, keyProperty = "id", keyColumn = "id")
    @Insert("insert into ctask (order_id, source_json, type, state, create_user, result_json, middle_json, create_time, update_time , tag_middle)" +
            " values (#{orderId}, #{sourceJson}, #{type}, #{state}, #{createUser}, #{resultJson}, #{middleJson}, #{createTime}, #{updateTime} , 0)")
    void addTask(Task task);

    @Update("update ctask set state = '整托计算完成', result_json = #{jsonPath} ,result_excel = #{excelPath} , update_time = now() where id = #{taskId}")
    void updateTask(Integer taskId, String jsonPath , String excelPath);

    List<TaskDTO> list(Integer id, String type, String state, String orderId , String startTime , String endTime);

    @Delete("delete from ctask where id = #{taskId}")
    void delete(Integer taskId);

    @Select("select * from ctask where id = #{taskId}")
    Task findTaskById(Integer taskId);

    @Update("update ctask set state = #{state}, update_time = now() where id = #{taskId}")
    void updateExecutionState(Integer taskId, String state);

    @Select("select * from ctask where create_user = #{currentUser} AND state = '整托计算完成' AND type = '托盘装箱' order by create_time desc limit 1")
    Task getPalletLatestTask(Integer currentUser);

    @Select("select * from ctask where create_user = #{currentUser} AND state = '悬空计算完成' AND type = '悬空装箱' order by create_time desc limit 1")
    Task getSuspandLatestTask(Integer currentUser);
}
