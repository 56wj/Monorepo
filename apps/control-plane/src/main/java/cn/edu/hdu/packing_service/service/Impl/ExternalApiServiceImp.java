package cn.edu.hdu.packing_service.service.Impl;
import cn.edu.hdu.packing_service.constant.StatusCodes;
import cn.edu.hdu.packing_service.mapper.ExternalApiMapper;
import cn.edu.hdu.packing_service.pojo.PushTask;
import cn.edu.hdu.packing_service.service.ExternalApiService;
import cn.edu.hdu.packing_service.utils.DateUtil;
import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.parser.Feature;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.jdbc.DataSourceTransactionManagerAutoConfiguration;
import org.springframework.stereotype.Service;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;


@Service
public class ExternalApiServiceImp implements ExternalApiService {

    @Autowired
    private ExternalApiMapper externalApiMapper;
    @Autowired
    private DataSourceTransactionManagerAutoConfiguration dataSourceTransactionManagerAutoConfiguration;

    @Override
    public Integer addTask(String orderID, String type, String data) {

        PushTask pushTask = new PushTask();

        pushTask.setOrderId(orderID);
        pushTask.setType(type);
        pushTask.setOrderData(data);
        pushTask.setReadStatus(0);
        pushTask.setPushTime(LocalDateTime.now());

        externalApiMapper.addTask(pushTask);
        return pushTask.getPid();
    }

    @Override
    public JSONObject getTask(Integer pushId) {
        //返回结果Json格式
        JSONObject res = new JSONObject(true);
        //获取任务
        PushTask pushTask = externalApiMapper.getTask(pushId);
        //判断是否存在
        if (pushTask == null) {
            System.out.println(DateUtil.getNowTime() + " - " + "任务 " + pushId + "不存在");
            res.put("error", StatusCodes.TASK_NULL_ERROR);
            return res;
        }else {
            System.out.println(DateUtil.getNowTime() + " - " + "获取任务 " + pushId);
            //将任务转换为Json格式
            res.put("pid" , pushTask.getPid());
            res.put("orderId" , pushTask.getOrderId());
            res.put("type" , pushTask.getType());
            res.put("readStatus" , pushTask.getReadStatus());
            res.put("pushTime" , pushTask.getPushTime());

            //获取orderData对应地址文件数据
            String orderDataPath = pushTask.getOrderData();
            String orderData = "";
            try {
                orderData = new String(Files.readAllBytes(Paths.get(orderDataPath)));
            } catch (Exception e) {
                res.put("error", StatusCodes.FILE_READ_ERROR);
                return res;
            }
            JSONObject sourceJsonObj = JSONObject.parseObject(orderData, Feature.OrderedField);
            res.put("orderData" , sourceJsonObj);

            //更新任务状态
            externalApiMapper.updateTaskStatus(pushId);
            System.out.println(DateUtil.getNowTime() + " - " + "已更新 " + pushId + " 读取状态");
        }
        return res;
    }
}
