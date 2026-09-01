package cn.edu.hdu.packing_service.service.Impl;

import cn.edu.hdu.packing_service.config.PythonExecuteConfig;
import cn.edu.hdu.packing_service.mapper.TaskMapper;
import cn.edu.hdu.packing_service.pojo.PageBean;
import cn.edu.hdu.packing_service.pojo.Task;
import cn.edu.hdu.packing_service.pojo.dto.TaskDTO;
import cn.edu.hdu.packing_service.service.TaskService;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

@Service
public class TaskServiceImpl implements TaskService {

    @Autowired
    private PythonExecuteConfig pythonExecuteConfig; // python接口配置

    @Autowired
    private TaskMapper taskMapper;

    @Override
    public PageBean<TaskDTO> list(Integer pageNum, Integer pageSize, String type, String state , String orderId , String startTime , String endTime) {
        //创建PageBean对象
        PageBean<TaskDTO> res = new PageBean<>();

        //开启分页查询 PageHelper
        PageHelper.startPage(pageNum, pageSize);

        //获取用户id
        Map<String ,Object> claims = ThreadLocalUtil.get();
        Integer id = (Integer) claims.get("id");

        if (endTime != null && !endTime.equals("")){
            ZonedDateTime zonedDateTime = ZonedDateTime.parse(endTime);
            ZonedDateTime plusDays = zonedDateTime.plusDays(1);
            ZonedDateTime minusOneSecond = plusDays.minusSeconds(1);
            endTime = minusOneSecond.format(DateTimeFormatter.ISO_INSTANT);
        }

        //调用Mapper
        List<TaskDTO> taskList = taskMapper.list(id ,type , state,orderId , startTime , endTime);

        Page<TaskDTO> p = (Page<TaskDTO>) taskList;
        res.setTotal(p.getTotal());
        res.setItems(p.getResult());

        return res;
    }

    @Override
    public Task findById(Integer taskId) {
        return taskMapper.findTaskById(taskId);
    }

    @Override
    public void delete(Task task) throws IOException {
        //获取文件路径
        String  source_path = task.getSourceJson();
        String  result_path = task.getResultJson();
        String  midlle_path = task.getMiddleJson();

        //删除result中的图片
        //获取任务id
        Integer taskId = task.getId();
        //构建图片地址
        Path imgPath = Paths.get(pythonExecuteConfig.getImage_path() + taskId.toString());
        System.out.println(imgPath);
        //删除文件夹
        if (Files.exists(imgPath)) {  // 确保路径存在
            try (Stream<Path> walk = Files.walk(imgPath)) {
                walk.sorted(Comparator.reverseOrder())  // 重要：需要反向排序，先删除文件，最后删除文件夹
                        .forEach(p -> {
                            try {
                                Files.delete(p);  // 删除每一个子路径
                            } catch (IOException e) {
                                System.err.println("Failed to delete " + p + " due to " + e.getMessage());
                            }
                        });
            }
        } else {
            System.out.println("File or Directory does not exist: " + imgPath);
        }

        //删除源文件
        if (source_path != null){
            if (Files.exists(Paths.get(source_path))){
                Files.delete(Paths.get(source_path));
                System.out.println("源文件" + source_path + "已删除");
            }else {
                System.out.println("源文件" + source_path + "不存在");
            }
        }
        //删除结果文件
        if (result_path != null){
            if (Files.exists(Paths.get(result_path))){
                Files.delete(Paths.get(result_path));
                System.out.println("结果文件" + result_path + "已删除");
            }else {
                System.out.println("结果文件" + result_path + "不存在");
            }
        }
        //删除中间文件
        if (midlle_path != null){
            if (Files.exists(Paths.get(midlle_path))){
                Files.delete(Paths.get(midlle_path));
                System.out.println("中间文件" + midlle_path + "已删除");
            }else {
                System.out.println("中间文件" + midlle_path + "不存在");
            }
        }

        taskMapper.delete(task.getId());
    }

    @Override
    public void batchDelete(List<Integer> taskIds) throws IOException {
        for (Integer taskId : taskIds) {
            Task task = taskMapper.findTaskById(taskId);
            delete(task);
        }
    }

    @Override
    public Task getPalletLatestTask() {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer currentUser = (Integer) claims.get("id");

        //获取最新的任务
        return taskMapper.getPalletLatestTask(currentUser);

    }

    @Override
    public Task getSuspandLatestTask() {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer currentUser = (Integer) claims.get("id");

        //获取最新的任务
        return taskMapper.getSuspandLatestTask(currentUser);

    }

}
