package cn.edu.hdu.packing_service.controller;

import cn.edu.hdu.packing_service.job.*;
import cn.edu.hdu.packing_service.job.dto.JobView;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.service.TaskService;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.server.ResponseStatusException;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class TaskJobQueryTest {
    private final TaskController controller = new TaskController();
    private final TaskService tasks = mock(TaskService.class);
    private final JobQueueService jobs = mock(JobQueueService.class);
    private final ObjectMapper json = new ObjectMapper();
    private PackingJob job;

    @BeforeEach void setup() throws Exception {
        ReflectionTestUtils.setField(controller, "taskService", tasks);
        ReflectionTestUtils.setField(controller, "jobQueueService", jobs);
        Task task = new Task(); task.setId(42); task.setCreateUser(9);
        when(tasks.findById(42)).thenReturn(task);
        ThreadLocalUtil.set(Collections.singletonMap("id", 9));
        job = new PackingJob(); job.setPublicId("job-42"); job.setTaskId(42);
        job.setJobType("PALLET_FIRST"); job.setStatus("SUCCEEDED");
        when(jobs.findLatestByTaskId(42)).thenReturn(job);
        when(jobs.payload(job)).thenReturn(json.readTree("{\"data\":{\"config\":{\"name\":\"first\"}}}"));
        when(jobs.result(job)).thenReturn(json.readTree("{\"result\":\"[]\"}"));
    }
    @AfterEach void clear() { ThreadLocalUtil.remove(); }

    @Test void ownerCanRecoverCompletedResultAndConfig() {
        JobView view = controller.job(42, true).getData();
        assertEquals("[]", view.getOutput().path("result").asText());
        assertEquals("first", view.getConfig().path("name").asText());
    }
    @Test void secondStageUsesSourceConfig() throws Exception {
        job.setJobType("PALLET_SECOND");
        when(jobs.payload(job)).thenReturn(json.readTree("{\"sourceJson\":{\"config\":{\"name\":\"second\"}}}"));
        assertEquals("second", controller.job(42, true).getData().getConfig().path("name").asText());
    }
    @Test void metadataOnlyQueryDoesNotLoadOutput() {
        assertNull(controller.job(42, false).getData().getOutput());
        verify(jobs, never()).result(any());
        verify(jobs, never()).payload(any());
    }
    @Test void anotherUserDoesNotReadJobOrResult() {
        ThreadLocalUtil.set(Collections.singletonMap("id", 10));
        assertEquals(404, assertThrows(ResponseStatusException.class, () -> controller.job(42, true)).getRawStatusCode());
        verify(jobs, never()).findLatestByTaskId(any());
        verify(jobs, never()).result(any());
    }
    @Test void missingIdentityIsRejected() {
        ThreadLocalUtil.remove();
        assertThrows(ResponseStatusException.class, () -> controller.job(42, true));
        verify(jobs, never()).findLatestByTaskId(any());
    }
    @Test void unknownTaskIsNotFound() {
        assertEquals(404, assertThrows(ResponseStatusException.class, () -> controller.job(99, true)).getRawStatusCode());
    }
    @Test void nonTerminalJobHasNoResult() {
        job.setStatus("RUNNING"); job.setResultJson("{\"result\":\"stale\"}");
        JobQueueService real = new JobQueueService(null, null, null, json, null);
        assertNull(real.result(job));
    }
    @Test void durableResultIsParsedOnlyForSuccess() {
        job.setResultJson("{\"result\":\"[]\"}");
        JobQueueService real = new JobQueueService(null, null, null, json, null);
        assertEquals("[]", real.result(job).path("result").asText());
        job.setResultJson("not-json");
        assertThrows(IllegalStateException.class, () -> real.result(job));
    }
}
