package cn.edu.hdu.packing_service.mapper;

import cn.edu.hdu.packing_service.pojo.User;
import org.apache.ibatis.annotations.*;

import java.util.List;

/**
 * @Author: ZhangWH
 * @Date: 2024/2/28 11:13
 */
@Mapper
public interface UserMapper {

    //根据用户名查询用户
    @Select("select * from user where username = #{username}")
    User queryUserByName(String username);

    @Insert("insert into user(username, password, email, phone, department, roles, create_time, update_time) values(#{username}, #{password}, #{email}, #{phone}, #{department}, #{roles}, now(), now())")
    void register(User user);

    @Update("update user set password = #{md5Pw} where id = #{uid}")
    void updatePassword(Integer uid, String md5Pw);

    @Select("select * from user where id = #{id}")
    User queryUserById(Integer id);

    @Update("update user set email = #{email}, phone = #{phone}, update_time = now() where id = #{id}")
    void updateUserInfo(User user);

    List<User> queryUserList(String username, String department, String role);

    @Delete("delete from user where id = #{uid}")
    void deleteUser(Integer uid);

    @Update("update user set username = #{username} , department = #{department} where id = #{id}")
    void adminUpdateUserInfo(User user);
}
