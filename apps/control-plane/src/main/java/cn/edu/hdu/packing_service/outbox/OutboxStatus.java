package cn.edu.hdu.packing_service.outbox;

public enum OutboxStatus {
    PENDING,
    PUBLISHING,
    PUBLISHED,
    DEAD_LETTER
}
