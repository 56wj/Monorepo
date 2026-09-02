package cn.edu.hdu.packing_service.job;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

@Component
public class WorkerTokenVerifier {
    private final JobQueueProperties properties;

    public WorkerTokenVerifier(JobQueueProperties properties) {
        this.properties = properties;
    }

    public void verify(String suppliedToken) {
        String expectedToken = properties.getWorkerToken();
        boolean valid = suppliedToken != null && expectedToken != null &&
                !suppliedToken.trim().isEmpty() && !expectedToken.trim().isEmpty() &&
                MessageDigest.isEqual(
                        expectedToken.getBytes(StandardCharsets.UTF_8),
                        suppliedToken.getBytes(StandardCharsets.UTF_8)
                );
        if (!valid) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "invalid worker token");
        }
    }
}
