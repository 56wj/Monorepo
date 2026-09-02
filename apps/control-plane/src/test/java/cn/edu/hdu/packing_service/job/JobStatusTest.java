package cn.edu.hdu.packing_service.job;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class JobStatusTest {

    @Test
    void queuedJobsCanOnlyRunOrBeCancelled() {
        assertTrue(JobStatus.QUEUED.canTransitionTo(JobStatus.RUNNING));
        assertTrue(JobStatus.QUEUED.canTransitionTo(JobStatus.CANCELLED));
        assertFalse(JobStatus.QUEUED.canTransitionTo(JobStatus.SUCCEEDED));
    }

    @Test
    void runningJobsCanRetryOrFinish() {
        assertTrue(JobStatus.RUNNING.canTransitionTo(JobStatus.RETRY_WAIT));
        assertTrue(JobStatus.RUNNING.canTransitionTo(JobStatus.SUCCEEDED));
        assertTrue(JobStatus.RUNNING.canTransitionTo(JobStatus.DEAD_LETTER));
    }

    @Test
    void terminalStatesCannotTransition() {
        for (JobStatus status : new JobStatus[]{JobStatus.SUCCEEDED, JobStatus.DEAD_LETTER, JobStatus.CANCELLED}) {
            for (JobStatus target : JobStatus.values()) {
                assertFalse(status.canTransitionTo(target));
            }
            assertTrue(status.isTerminal());
        }
    }
}
