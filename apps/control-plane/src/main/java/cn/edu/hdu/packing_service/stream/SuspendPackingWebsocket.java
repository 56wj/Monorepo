package cn.edu.hdu.packing_service.stream;

import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.stream.encoder.ResultEncoder;
import cn.edu.hdu.packing_service.utils.DateUtil;
import cn.edu.hdu.packing_service.utils.JwtUtil;
import org.springframework.stereotype.Component;

import javax.websocket.CloseReason;
import javax.websocket.EncodeException;
import javax.websocket.OnClose;
import javax.websocket.OnError;
import javax.websocket.OnMessage;
import javax.websocket.OnOpen;
import javax.websocket.Session;
import javax.websocket.server.ServerEndpoint;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@ServerEndpoint(value = "/suspendpackingWebsocket", encoders = {ResultEncoder.class})
@Component
public class SuspendPackingWebsocket {

    private static final long MAX_IDLE_TIMEOUT_MS = 90000L;

    public static final Map<String, Session> clients = new ConcurrentHashMap<>();
    public static final Map<String, Set<String>> conns = new ConcurrentHashMap<>();

    private String sid;
    private String userId;

    @OnOpen
    public void onOpen(Session session) throws IOException {
        String token = firstRequestParameter(session, "token");
        if (isBlank(token)) {
            session.close(new CloseReason(CloseReason.CloseCodes.VIOLATED_POLICY, "missing token"));
            return;
        }

        try {
            Map<String, Object> claims = JwtUtil.parseToken(token);
            Object currentUser = claims.get("id");
            if (currentUser == null) {
                session.close(new CloseReason(CloseReason.CloseCodes.VIOLATED_POLICY, "invalid token"));
                return;
            }

            this.sid = UUID.randomUUID().toString();
            this.userId = String.valueOf(currentUser);
            session.setMaxIdleTimeout(MAX_IDLE_TIMEOUT_MS);
            clients.put(this.sid, session);
            conns.computeIfAbsent(this.userId, key -> ConcurrentHashMap.newKeySet()).add(this.sid);
            System.out.println(DateUtil.getNowTime() + this.userId + "连接成功");
        } catch (RuntimeException error) {
            session.close(new CloseReason(CloseReason.CloseCodes.VIOLATED_POLICY, "invalid token"));
        }
    }

    @OnClose
    public void onClose(Session session, CloseReason reason) {
        removeSession(this.userId, this.sid, session);
    }

    public static boolean isServerClose() {
        boolean closed = clients.isEmpty();
        System.out.println(closed ? "已断开" : "已连接");
        return closed;
    }

    public static void sendMessage(String message) {
        System.out.println(DateUtil.getNowTime() + "悬空托盘信息发送给所有用户");
        for (Map.Entry<String, Session> entry : clients.entrySet()) {
            Session session = entry.getValue();
            if (session == null || !session.isOpen()) {
                clients.remove(entry.getKey(), session);
                continue;
            }
            try {
                synchronized (session) {
                    session.getBasicRemote().sendText(message);
                }
            } catch (IOException | RuntimeException error) {
                clients.remove(entry.getKey(), session);
                error.printStackTrace();
            }
        }
    }

    public static void sendMessageByUserId(String userId, Result message) {
        System.out.println(DateUtil.getNowTime() + "悬空托盘信息发送给用户" + userId);
        if (isBlank(userId)) return;

        Set<String> clientSet = conns.get(userId);
        if (clientSet == null) return;

        for (String sid : clientSet) {
            Session session = clients.get(sid);
            if (session == null || !session.isOpen()) {
                removeSession(userId, sid, session);
                continue;
            }
            try {
                synchronized (session) {
                    session.getBasicRemote().sendObject(message);
                }
            } catch (IOException | EncodeException | RuntimeException error) {
                removeSession(userId, sid, session);
                error.printStackTrace();
            }
        }
    }

    @OnMessage
    public void onMessage(String message, Session session) {
        System.out.println(DateUtil.getNowTime() + "悬空托盘收到来自窗口" + this.userId + "的信息:" + message);
    }

    @OnError
    public void onError(Session session, Throwable error) {
        removeSession(this.userId, this.sid, session);
        error.printStackTrace();
    }

    private static String firstRequestParameter(Session session, String name) {
        Map<String, List<String>> parameters = session.getRequestParameterMap();
        List<String> values = parameters.get(name);
        return values == null || values.isEmpty() ? null : values.get(0);
    }

    private static boolean isBlank(String value) {
        return value == null || value.trim().isEmpty();
    }

    private static void removeSession(String userId, String sid, Session session) {
        if (sid == null) return;

        if (session == null) {
            clients.remove(sid);
        } else {
            clients.remove(sid, session);
        }

        if (userId == null) return;
        Set<String> clientSet = conns.get(userId);
        if (clientSet == null) return;
        clientSet.remove(sid);
        if (clientSet.isEmpty()) {
            conns.remove(userId, clientSet);
        }
    }
}
