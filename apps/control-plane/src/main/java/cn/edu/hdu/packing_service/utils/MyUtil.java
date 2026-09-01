package cn.edu.hdu.packing_service.utils;

import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.util.Map;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/28 14:37
 */
@Component
public class MyUtil {

    private static PythonExecuteConfig pythonExecuteConfigStatic;

    private static UserService userServiceStatic;

    @Autowired
    private PythonExecuteConfig pythonExecuteConfig;

    @Autowired
    private UserService userService;

    @PostConstruct
    public void init() {
        pythonExecuteConfigStatic = pythonExecuteConfig;
        userServiceStatic = userService;
    }

    public static String getPythonExecuteUrl(){
        return pythonExecuteConfigStatic.getHost() + ":" + pythonExecuteConfigStatic.getPort();
    }

    //验证用户权限
    public static boolean checkUserPermission() {
        //TODO
        Boolean hasPermission;
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        hasPermission = userServiceStatic.hasPermission(userId);

        return hasPermission;
    }
}
