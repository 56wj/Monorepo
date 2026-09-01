package cn.edu.hdu.packing_service.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.ImportSelector;
import org.springframework.core.type.AnnotationMetadata;
import org.springframework.web.client.RestTemplate;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

/*本方法用于自动注入第三方类进入ioc容器中，需要在application文件前添加@Import(CommonImportSelector.class)
 同时在common.import文件中添加需要导入的包
 * */
@Configuration
public class CommonImportSelector implements ImportSelector {
    @Override
    public String[] selectImports(AnnotationMetadata importingClassMetadata) {

        List<String> imports = new ArrayList<>();
        InputStream is = CommonImportSelector.class.getClassLoader().getResourceAsStream("common.imports");
        BufferedReader br = new BufferedReader(new InputStreamReader(is));
        String line = null;
        try {
            while((line = br.readLine())!= null){
                imports.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null){
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return imports.toArray(new String[0]);
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
