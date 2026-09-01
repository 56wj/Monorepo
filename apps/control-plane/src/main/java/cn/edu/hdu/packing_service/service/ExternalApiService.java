package cn.edu.hdu.packing_service.service;

import com.alibaba.fastjson.JSONObject;

import java.util.Map;

public interface ExternalApiService {

    // 该方法用于向第三方系统发送任务
    Integer addTask(String orderID, String type, String string);

    // 该方法用于获取第三方系统发送的任务
    JSONObject getTask(Integer pushId);
}
