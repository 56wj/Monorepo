package cn.edu.hdu.packing_service.stream.encoder;

import cn.edu.hdu.packing_service.pojo.Result;
import com.alibaba.fastjson.JSONObject;

import javax.websocket.EncodeException;
import javax.websocket.Encoder;
import javax.websocket.EndpointConfig;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/22 19:22
 */
public class ResultEncoder implements Encoder.Text<Result> {



    @Override
    public void init(EndpointConfig endpointConfig) {

    }

    @Override
    public void destroy() {

    }

    @Override
    public String encode(Result result) throws EncodeException {

        try {
            return JSONObject.toJSONString(result);
        }catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }
}
