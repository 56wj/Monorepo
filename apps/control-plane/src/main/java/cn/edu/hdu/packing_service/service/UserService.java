package cn.edu.hdu.packing_service.service;

import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.pojo.User;

import java.util.List;

/**
 * @Author: ZhangWH
 * @Date: 2024/2/28 11:12
 */
public interface UserService {

    //根据用户名查询用户
    User queryUserByName(String username);

    //注册用户
    void register(User user);

    //修改密码
    void updatePassword(Integer uid, String newPassword);

    //根据id查询用户
    User queryUserById(Integer id);

    //更新用户信息
    void updateUserInfo(User user);

    //判断用户是否有权限
    Boolean hasPermission(Integer userId);

    //查询用户列表
    PageBean<User> queryUserList(Integer pageNum, Integer pageSize, String username, String department, String role);

    //删除用户
    void deleteUser(Integer uid);

    //批量删除用户
    void deleteUsers(List<Integer> uids);

    //管理员修改用户信息
    void adminUpdateUserInfo(User user);
}
