package cn.edu.hdu.packing_service;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class PackingServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(PackingServiceApplication.class, args);
    }

}
