package cn.edu.hdu.packing_service.job;

import org.junit.jupiter.api.Test;
import org.springframework.web.server.ResponseStatusException;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertThrows;

class WorkerTokenVerifierTest {

    @Test
    void acceptsOnlyTheConfiguredNonEmptyToken() {
        JobQueueProperties properties = new JobQueueProperties();
        properties.setWorkerToken("worker-secret");
        WorkerTokenVerifier verifier = new WorkerTokenVerifier(properties);

        assertDoesNotThrow(() -> verifier.verify("worker-secret"));
        assertThrows(ResponseStatusException.class, () -> verifier.verify("wrong"));
        assertThrows(ResponseStatusException.class, () -> verifier.verify(null));
    }

    @Test
    void emptyConfiguredTokenDoesNotDisableAuthentication() {
        JobQueueProperties properties = new JobQueueProperties();
        properties.setWorkerToken("");
        WorkerTokenVerifier verifier = new WorkerTokenVerifier(properties);

        assertThrows(ResponseStatusException.class, () -> verifier.verify(""));
    }
}
