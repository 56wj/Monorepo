package cn.edu.hdu.packing_service.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface SuspendMapper {

    @Update("update ctask set state = '悬空计算完成', result_json = #{jsonPath} , update_time = now() ,tag_middle = 1 where id = #{taskId}")
    void updateTask(int taskId, String jsonPath);
}
