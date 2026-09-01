package cn.edu.hdu.packing_service.controller;

import cn.edu.hdu.packing_service.Annotation.MyAnnotation;
import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.utils.JwtUtil;
import cn.edu.hdu.packing_service.utils.Md5Util;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.pojo.User;
import cn.edu.hdu.packing_service.service.UserService;
import cn.edu.hdu.packing_service.utils.MyUtil;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.constraints.Pattern;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @Author: ZhangWH
 * @Date: 2024/2/28 11:00
 */
@Validated
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    UserService userService;

    //注册
    @PostMapping("/register")
    public Result register(@Pattern(regexp = "^\\S{5,16}$") String username, @Pattern(regexp = "^\\S{5,16}$") String password) {
        //查询用户
        User u = userService.queryUserByName(username);
        System.out.println("u = " + u);
        if (u == null) { //用户未被占用
            //注册用户
//            userService.register(username, password);
            return Result.success();
        }else { //用户已被占用
            return Result.error("用户名已存在");
        }
    }

    //登录
    @PostMapping("/login")
    public Result<String> login(@Pattern(regexp = "^\\S{5,16}$") String username, @Pattern(regexp = "^\\S{5,16}$") String password) {
        User loginuser = userService.queryUserByName(username);
        if (loginuser == null) {
            return Result.error("用户不存在");
        } else if (Md5Util.checkPassword(password , loginuser.getPassword())) {
            Map<String , Object> claims = new HashMap<>();
            claims.put("id" , loginuser.getId());
            claims.put("username" , loginuser.getUsername());
            String token = JwtUtil.genToken(claims);

            return Result.success(token);
        } else {
            return Result.error("密码错误");
        }
    }

    //获取用户详细信息
    @GetMapping("/userInfo")
    public Result<Map<String , Object>> userInfo() {
        Map<String , Object> claims = ThreadLocalUtil.get();
        String username = (String)claims.get("username");
        User user = userService.queryUserByName(username);
        Map<String , Object> res = new HashMap<>();
        res.put("userInfo" , user);
        //添加python执行地址
        res.put("pythonExecuteUrl" , MyUtil.getPythonExecuteUrl());
        return Result.success(res);
    }

    //修改密码
    @PutMapping("/updatePassword")
    public Result updatePassword(@Pattern(regexp = "^\\S{5,16}$") String oldPassword, @Pattern(regexp = "^\\S{5,16}$") String newPassword) {
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer uid = (Integer)claims.get("id");
        User user = userService.queryUserById(uid);
        if (Md5Util.checkPassword(oldPassword , user.getPassword())){
            userService.updatePassword(uid , newPassword);
            return Result.success();
        } else {
            return Result.error("原密码错误");
        }
    }

    //更新用户信息
    @PostMapping("/updateUserInfo")
    public Result updateUserInfo(@RequestBody @Validated(User.Update.class) User user){
        userService.updateUserInfo(user);
        return Result.success();
    }

    //获取用户列表
    @MyAnnotation(moudle = "用户",operate = "获取全部用户")
    @GetMapping("/userList")
    public Result userList(Integer pageNum , Integer pageSize,
                           @Pattern(regexp = "^\\S*$") @RequestParam(required = false) String username,
                           @RequestParam(required = false) String department,
                           @RequestParam(required = false) String role) {
        PageBean<User> userList = userService.queryUserList(pageNum , pageSize , username , department , role);
        System.out.println(userList);
        return Result.success(userList);
    }

    //管理员修改用户密码
    @PutMapping("/adminUpdatePassword")
    public Result adminUpdatePassword(Integer uid , @Pattern(regexp = "^\\S{5,16}$") String newPassword) {
        //验证管理员权限
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        Boolean hasPermission = userService.hasPermission(userId);
        if (!hasPermission) {
            return Result.error("权限不足");
        }

        userService.updatePassword(uid , newPassword);
        return Result.success();
    }

    //管理员删除用户
    @DeleteMapping("/deleteUser")
    public Result deleteUser(Integer uid) {
        //验证管理员权限
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        Boolean hasPermission = userService.hasPermission(userId);
        if (!hasPermission) {
            return Result.error("权限不足");
        }

        userService.deleteUser(uid);
        return Result.success();
    }

    //管理员添加用户
    @PostMapping("/addUser")
    public Result addUser(@RequestBody @Validated(User.Add.class) User user) {
        //验证管理员权限
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        Boolean hasPermission = userService.hasPermission(userId);
        if (!hasPermission) {
            return Result.error("权限不足");
        }

        //查询用户
        User u = userService.queryUserByName(user.getUsername());
        if (u == null) { //用户未被占用
            //注册用户
            userService.register(user);
            return Result.success();
        }else { //用户已被占用
            return Result.error("用户名已存在");
        }
    }

    //批量删除用户
    @DeleteMapping("/deleteUsers")
    public Result deleteUsers(@RequestBody List<Integer> uids) {
        //验证管理员权限
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        Boolean hasPermission = userService.hasPermission(userId);
        if (!hasPermission) {
            return Result.error("权限不足");
        }

        userService.deleteUsers(uids);
        return Result.success();
    }

    //管理员修改用户信息
    @PutMapping("/adminUpdateUserInfo")
    public Result adminUpdateUserInfo(@RequestBody @Validated(User.AdminUpdate.class) User user) {
        //验证管理员权限
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        Boolean hasPermission = userService.hasPermission(userId);
        if (!hasPermission) {
            return Result.error("权限不足");
        }

        userService.adminUpdateUserInfo(user);
        return Result.success();
    }

}
