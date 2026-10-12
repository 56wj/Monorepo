package cn.edu.hdu.packing_service.notification;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
public class TaskNotificationConfiguration {
    @Bean("taskNotificationExecutor")
    public ThreadPoolTaskExecutor taskNotificationExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(1);
        executor.setMaxPoolSize(2);
        executor.setQueueCapacity(64);
        executor.setThreadNamePrefix("task-notify-");
        executor.setWaitForTasksToCompleteOnShutdown(false);
        return executor;
    }
}
