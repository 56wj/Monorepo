package cn.edu.hdu.packing_service.mapper;

import cn.edu.hdu.packing_service.pojo.Department;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/18 10:09
 */

@Mapper
public interface DepartmentMapper {

    @Select("select * from department")
    List<Department> queryAll();

    @Select("insert into department(department_name,create_time,update_time) values(#{departmentName},#{createTime},#{updateTime})")
    void add(Department department);

    @Update("update department set department_name = #{departmentName},update_time = #{updateTime} where department_id = #{departmentId}")
    void update(Department department);

    @Select("select * from department where department_id = #{departmentId}")
    Department queryById(Integer id);

    @Delete("delete from department where department_id = #{departmentId}")
    void delete(Integer id);

}
