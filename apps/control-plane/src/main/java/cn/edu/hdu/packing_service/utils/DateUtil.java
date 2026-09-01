package cn.edu.hdu.packing_service.utils;

import java.time.LocalDateTime;

public class DateUtil {

    /**
     * @Author: strelizia
     * @Date: 2024/1/30 12:06
     * @return: String
     * @Description: 获取当前时间
     */
    public static String getNowTime(){
        return "time:   " + LocalDateTime.now().toString() + "  ";
    }
}
