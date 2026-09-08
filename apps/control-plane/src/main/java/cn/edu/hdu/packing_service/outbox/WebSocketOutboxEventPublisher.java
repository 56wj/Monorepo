package cn.edu.hdu.packing_service.outbox;

import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.stream.PalletPackingWebsocket;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

@Component
public class WebSocketOutboxEventPublisher implements OutboxEventPublisher {
    private final ObjectMapper objectMapper;

    public WebSocketOutboxEventPublisher(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    @Override
    public void publish(OutboxEvent event) throws Exception {
        JsonNode payload = objectMapper.readTree(event.getPayloadJson());
        if (payload == null || !payload.isObject() || !payload.hasNonNull("code")) {
            throw new IllegalArgumentException("Outbox notification payload is invalid");
        }
        Object data = payload.has("data") && !payload.get("data").isNull()
                ? objectMapper.treeToValue(payload.get("data"), Object.class)
                : null;
        Result<Object> notification = new Result<>(
                payload.get("code").asInt(),
                payload.path("message").asText(""),
                data
        );
        PalletPackingWebsocket.sendMessageByUserIdOrThrow(event.getUserId(), notification);
    }
}
