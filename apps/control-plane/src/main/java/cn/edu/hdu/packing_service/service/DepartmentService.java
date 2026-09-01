package cn.edu.hdu.packing_service.service;

import cn.edu.hdu.packing_service.pojo.Department;

import java.util.List;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/18 10:07
 */
public interface DepartmentService {

    //查询所有部门
    List<Department> queryAll();

    //添加部门
    void add(Department department);

    //修改部门
    void update(Department department);

    //删除部门
    void delete(Integer id);
}
