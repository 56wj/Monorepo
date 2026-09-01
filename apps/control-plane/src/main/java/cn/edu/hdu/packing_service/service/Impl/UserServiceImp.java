package cn.edu.hdu.packing_service.service.Impl;

import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;
import cn.edu.hdu.packing_service.utils.Md5Util;
import cn.edu.hdu.packing_service.mapper.UserMapper;
import cn.edu.hdu.packing_service.pojo.User;
import cn.edu.hdu.packing_service.service.UserService;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

/**
 * @Author: ZhangWH
 * @Date: 2024/2/28 11:12
 */

@Service
public class UserServiceImp implements UserService {

    @Autowired
    UserMapper userMapper;

    @Override
    public User queryUserByName(String username) {
        User user = userMapper.queryUserByName(username);
        if (user != null && user.getRoles() != null) {
            List<String> rolesList = Arrays.asList(user.getRoles().split(","));
            user.setRolesList(rolesList); // 假设你添加了这个不映射数据库的辅助字段或者通过其他方式处理
        }
        return user;
    }


    @Override
    public void register(User user) {
        String md5Pw = Md5Util.getMD5String(user.getPassword());
        user.setPassword(md5Pw);
        userMapper.register(user);
    }

    @Override
    public void updatePassword(Integer uid, String newPassword) {
        String md5Pw = Md5Util.getMD5String(newPassword);
        userMapper.updatePassword(uid, md5Pw);
    }

    @Override
    public User queryUserById(Integer id) {
        User user = userMapper.queryUserById(id);
        if (user != null && user.getRoles() != null) {
            List<String> rolesList = Arrays.asList(user.getRoles().split(","));
            user.setRolesList(rolesList); // 假设你添加了这个不映射数据库的辅助字段或者通过其他方式处理
        }
        return user;
    }

    @Override
    public void updateUserInfo(User user) {
        // 通过ThreadLocal获取当前登录用户的id
        Map<String, Object> claims = ThreadLocalUtil.get();
        Integer id = (Integer) claims.get("id");
        user.setId(id);
        userMapper.updateUserInfo(user);
    }

    @Override
    public Boolean hasPermission(Integer userId) {
        User user = userMapper.queryUserById(userId);
        if (user.getRoles().equals("admin")) {
            return true;
        }
        return false;
    }

    @Override
    public PageBean<User> queryUserList(Integer pageNum, Integer pageSize, String username, String department, String role) {
        //创建PageBean对象
        PageBean<User> res = new PageBean<>();

        //开启分页查询 PageHelper
        PageHelper.startPage(pageNum, pageSize);


        //调用Mapper
        List<User> userList = userMapper.queryUserList(username, department, role);

        Page<User> p = (Page<User>) userList;
        res.setTotal(p.getTotal());
        res.setItems(p.getResult());

        return res;
    }

    @Override
    public void deleteUser(Integer uid) {
        userMapper.deleteUser(uid);
    }

    @Override
    public void deleteUsers(List<Integer> uids) {
        for (Integer uid : uids) {
            userMapper.deleteUser(uid);
        }
    }

    @Override
    public void adminUpdateUserInfo(User user) {
        userMapper.adminUpdateUserInfo(user);
    }
}
