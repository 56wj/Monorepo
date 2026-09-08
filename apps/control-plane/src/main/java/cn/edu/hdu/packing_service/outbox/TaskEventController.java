package cn.edu.hdu.packing_service.outbox;

import cn.edu.hdu.packing_service.outbox.dto.OutboxEventView;
import cn.edu.hdu.packing_service.outbox.dto.TaskEventPage;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/task/events")
public class TaskEventController {
    private final OutboxService service;

    public TaskEventController(OutboxService service) {
        this.service = service;
    }

    /**
     * Durable catch-up endpoint for a WebSocket reconnect. The opaque numeric
     * cursor is scoped to the authenticated user by the query itself.
     */
    @GetMapping
    public Result<TaskEventPage> list(@RequestParam(defaultValue = "0") long after,
                                      @RequestParam(defaultValue = "100") int limit) {
        Map<String, Object> claims = ThreadLocalUtil.get();
        String userId = String.valueOf(claims.get("id"));
        List<OutboxEvent> events = service.listForUserAfter(userId, after, limit);
        List<OutboxEventView> views = new ArrayList<>();
        long nextCursor = Math.max(0, after);
        for (OutboxEvent event : events) {
            views.add(OutboxEventView.from(event, service.payload(event)));
            nextCursor = Math.max(nextCursor, event.getId());
        }
        return Result.success(new TaskEventPage(nextCursor, views));
    }
}
