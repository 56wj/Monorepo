package cn.edu.hdu.packing_service.outbox.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

@Data
@AllArgsConstructor
public class TaskEventPage {
    private Long nextCursor;
    private List<OutboxEventView> events;
}
