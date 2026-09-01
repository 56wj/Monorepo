package cn.edu.hdu.packing_service.mapper;

import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;
import org.apache.ibatis.annotations.*;

import java.util.List;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/5 12:42
 */

@Mapper
public interface PalletPackingMapper {


    @Options(useGeneratedKeys = true, keyProperty = "id", keyColumn = "id")
    @Insert("insert into ctask (order_id, source_json, type, state, create_user, result_json, middle_json, create_time, update_time , tag_middle)" +
            " values (#{orderId}, #{sourceJson}, #{type}, #{state}, #{createUser}, #{resultJson}, #{middleJosn}, #{createTime}, #{updateTime} , 0)")
    void addTask(Task task);

    @Update("update ctask set state = '整托计算完成', result_json = #{jsonPath} ,result_excel = #{excelPath} , update_time = now() where id = #{taskId}")
    void updateTask(Integer taskId, String jsonPath , String excelPath);

    List<TaskDTO> list(Integer id, String type, String state,String orderId , String startTime , String endTime);

    @Delete("delete from ctask where id = #{taskId}")
    void delete(Integer taskId);

    @Select("select * from ctask where id = #{taskId}")
    Task findTaskById(Integer taskId);

    @Update("update ctask set state = '计算超时' where id = #{taskId}")
    void timeOut(Integer taskId);

    @Update("update ctask set state = '网络错误' where id = #{taskId}")
    void connectError(Integer taskId);

    @Select("select * from ctask where create_user = #{currentUser} AND state = '整托计算完成' order by create_time desc limit 1")
    Task getLatestTask(Integer currentUser);

    @Update("update ctask set state = '二阶段计算中', middle_json = #{storePath} , update_time = now() where id = #{taskId}")
    void secondUpdate(String storePath, Integer taskId);

    @Update("update ctask set state = '小托计算完成', update_time = now() ,tag_middle = 1 where id = #{taskId}")
    void updateFirst(int taskId, String result);
}
