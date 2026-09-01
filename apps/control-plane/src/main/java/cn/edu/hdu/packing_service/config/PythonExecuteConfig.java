package cn.edu.hdu.packing_service.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;


@Configuration
@Data
@ConfigurationProperties(prefix = "packing-python-api")
public class PythonExecuteConfig {
    private String host;
    private String port;
    private String route;
    private String methods;
    private String image_path;
    private String source_save_path;
    private String middle_save_path;
    private String result_save_path;
    private String push_save_path;

}
