package cn.edu.hdu.packing_service.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.groups.Default;
import java.time.LocalDateTime;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/5 12:29
 */
@AllArgsConstructor
@NoArgsConstructor
@Data
public class Task {

    public interface Update extends Default {}

    public interface Add extends Default{}

    @NotNull(groups = {Update.class})
    private Integer id; //主键ID

    @NotNull(groups = {Add.class})
    private String orderId; //订单ID

    private String sourceJson; //源json

    @NotNull(groups = {Add.class})
    private String type; //类型

    @NotNull(groups = {Update.class})
    private String state; //状态

    private Integer createUser; //创建人

    private String resultJson; //结果json

    private Integer tagMiddle; //一阶段tag

    private String middleJson; //中间json

    private String resultExcel; //结果excel

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updateTime;

}
