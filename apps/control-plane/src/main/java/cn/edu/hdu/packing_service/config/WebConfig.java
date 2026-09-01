package cn.edu.hdu.packing_service.config;


import cn.edu.hdu.packing_service.interceptors.LoginInterceptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * @Author: ZhangWH
 * @Date: 2024/2/13 21:42
 */

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Autowired
    private LoginInterceptor loginInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {

        //登录接口和注册接口不需要拦截
        registry.addInterceptor(loginInterceptor).excludePathPatterns("/user/login" , "/user/register" ,
                "/palletpacking/resultback_first","/specification/queryAll","/palletpacking/resultback_second","/specification/palletroll/queryByPalletId","/specification/tube/queryAll",
                "/specification/pallet/queryById","/specification/truck/queryAll","/externalApi/stock/push_data","/suspend/resultback_first","/externalApi/stock/push_data");

    }
}
