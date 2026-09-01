package cn.edu.hdu.packing_service.controller;

import cn.edu.hdu.packing_service.pojo.Department;
import cn.edu.hdu.packing_service.pojo.Result;
import cn.edu.hdu.packing_service.service.DepartmentService;
import cn.edu.hdu.packing_service.utils.MyUtil;
import org.apache.dubbo.config.ApplicationConfig;
import org.apache.dubbo.config.ConsumerConfig;
import org.apache.dubbo.config.ProtocolConfig;
import org.apache.dubbo.config.ReferenceConfig;
import org.apache.dubbo.rpc.service.GenericService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/18 9:55
 */
@RestController
@RequestMapping("/department")
public class DepartmentController {

    @Autowired
    DepartmentService departmentService;

    @Autowired
    private RestTemplate restTemplate;



    //查询所有部门
    @GetMapping("/queryAll")
    public Result queryAll() {
        List<Department> departmentList = departmentService.queryAll();
        return Result.success(departmentList);
    }

    //添加部门
    @PostMapping("/add")
    public Result add(@RequestBody @Validated(Department.Add.class) Department department) {
        //验证用户权限
        boolean isPermission = MyUtil.checkUserPermission();
        if (!isPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该部门
        List<Department> departmentList = departmentService.queryAll();
        for (Department tmp : departmentList) {
            if (tmp.getDepartmentName().equals(department.getDepartmentName())) {
                return Result.error("部门已存在");
            }
        }

        //添加部门
        departmentService.add(department);
        return Result.success();
    }

    //修改部门
    @PostMapping("/update")
    public Result update(@RequestBody @Validated(Department.Update.class) Department department) {
        //验证用户权限
        boolean isPermission = MyUtil.checkUserPermission();
        if (!isPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该部门
        List<Department> departmentList = departmentService.queryAll();
        for (Department tmp : departmentList) {
            if (tmp.getDepartmentName().equals(department.getDepartmentName()) && !tmp.getDepartmentId().equals(department.getDepartmentId())) {
                return Result.error("部门已存在");
            }
        }

        departmentService.update(department);
        return Result.success();
    }

    //删除部门
    @DeleteMapping("/delete")
    public Result delete(Integer id){
        //验证用户权限
        boolean isPermission = MyUtil.checkUserPermission();
        if (!isPermission) {
            return Result.error("没有权限");
        }

        departmentService.delete(id);
        return Result.success();
    }




    //Test
    @GetMapping("/test")
    public Result test() {

        System.out.println("java service start...");
        String url = "http://python-server/get_server_info";
        // 发送http请求，实现远程调用
        String ps = restTemplate.getForObject(url, String.class);
        System.out.println("Python service 返回内容: 【 " + ps + "】");
        return Result.success(ps);
    }

//    @GetMapping("/test")
//    public String test() {
//        // 创建应用配置
//        ApplicationConfig application = new ApplicationConfig();
//        application.setName("java-client");
//
//        // 配置连接参数
//        ReferenceConfig<GenericService> reference = new ReferenceConfig<>();
//        reference.setApplication(application);
//        reference.setInterface("org.apache.dubbo.samples.HelloWorld");
//        reference.setProtocol("tri");  // 使用 Triple 协议
//        Map<String, String> parameters = new HashMap<>();
//        parameters.put("tri.enabled", "true");
//        parameters.put("tri.default.protocol", "http");
//        reference.setParameters(parameters);
//
//        // 确保使用直连模式
//        reference.setUrl("tri://localhost:8849");
//        reference.setGeneric("true");  // 使用泛化调用
//        reference.setTimeout(10000);  // 超时时间设为 10 秒
//
//        StringBuilder result = new StringBuilder();
//
//        try {
//            // 获取泛化服务
//            GenericService genericService = reference.get();
//            result.append("连接已建立，开始调用服务\n");
//
//            // 调用 unary 方法
//            try {
//                long startTime = System.currentTimeMillis();
//                Object response = genericService.$invoke("unary",
//                        new String[]{"java.lang.String"},
//                        new Object[]{"Hello from Java client"});
//
//                result.append("调用 unary 成功！\n");
//                result.append("- 响应：").append(response).append("\n");
//                result.append("- 耗时：").append(System.currentTimeMillis() - startTime).append("ms\n\n");
//            } catch (Exception e) {
//                result.append("调用 unary 失败：").append(e.getMessage()).append("\n");
//                result.append("- 异常类型：").append(e.getClass().getName()).append("\n\n");
//            }
//
//            // 调用 ldrsb 方法
//            try {
//                long startTime = System.currentTimeMillis();
//                Object response = genericService.$invoke("ldrsb",
//                        new String[]{"java.lang.String"},
//                        new Object[]{"Hello from Java client for ldrsb"});
//
//                result.append("调用 ldrsb 成功！\n");
//                result.append("- 响应：").append(response).append("\n");
//                result.append("- 耗时：").append(System.currentTimeMillis() - startTime).append("ms\n");
//            } catch (Exception e) {
//                result.append("调用 ldrsb 失败：").append(e.getMessage()).append("\n");
//                result.append("- 异常类型：").append(e.getClass().getName()).append("\n");
//                e.printStackTrace();
//            }
//
//        } catch (Exception e) {
//            result.append("服务连接或初始化失败：").append(e.getMessage()).append("\n");
//            e.printStackTrace();
//        } finally {
//            // 确保销毁引用，释放资源
//            if (reference != null) {
//                reference.destroy();
//            }
//        }
//
//        return result.toString();
//    }
}
