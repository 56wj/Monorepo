package cn.edu.hdu.packing_service.notification;

import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.stream.PalletPackingWebsocket;
import org.springframework.stereotype.Component;

import java.util.Collections;

@Component
public class TaskNotificationSender {
    public void send(String userId, Integer taskId) throws Exception {
        // This is an invalidation hint, never the authoritative computation result.
        PalletPackingWebsocket.sendMessageByUserIdOrThrow(userId,
                Result.success(20000, "任务状态已更新", Collections.singletonMap("taskId", taskId)));
    }
}
