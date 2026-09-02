package cn.edu.hdu.packing_service.job;

import java.util.EnumSet;
import java.util.Set;

public enum JobStatus {
    QUEUED,
    RUNNING,
    RETRY_WAIT,
    SUCCEEDED,
    DEAD_LETTER,
    CANCELLED;

    public boolean canTransitionTo(JobStatus target) {
        Set<JobStatus> allowed;
        switch (this) {
            case QUEUED:
                allowed = EnumSet.of(RUNNING, CANCELLED);
                break;
            case RUNNING:
                allowed = EnumSet.of(SUCCEEDED, RETRY_WAIT, DEAD_LETTER, CANCELLED);
                break;
            case RETRY_WAIT:
                allowed = EnumSet.of(RUNNING, CANCELLED);
                break;
            default:
                allowed = EnumSet.noneOf(JobStatus.class);
        }
        return allowed.contains(target);
    }

    public boolean isTerminal() {
        return this == SUCCEEDED || this == DEAD_LETTER || this == CANCELLED;
    }
}
