package cn.edu.hdu.packing_service.service.Impl;

import cn.edu.hdu.packing_service.mapper.DepartmentMapper;
import cn.edu.hdu.packing_service.pojo.Department;
import cn.edu.hdu.packing_service.service.DepartmentService;
import cn.edu.hdu.packing_service.utils.MyUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/18 10:07
 */

@Service
public class DepartmentServiceImp implements DepartmentService {

    @Autowired
    DepartmentMapper departmentMapper;

    @Override
    public List<Department> queryAll() {
        return departmentMapper.queryAll();
    }

    @Override
    public void add(Department department) {

        department.setCreateTime(LocalDateTime.now());
        department.setUpdateTime(LocalDateTime.now());
        departmentMapper.add(department);
    }

    @Override
    public void update(Department department) {
        department.setUpdateTime(LocalDateTime.now());
        departmentMapper.update(department);
    }

    @Override
    public void delete(Integer id) {
        departmentMapper.delete(id);
    }


}
