package cn.edu.hdu.packing_service.outbox;

import lombok.Data;

@Data
public class OutboxStatusCount {
    private String status;
    private Long count;
}
