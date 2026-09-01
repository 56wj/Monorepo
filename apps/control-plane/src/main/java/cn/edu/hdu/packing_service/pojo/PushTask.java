package cn.edu.hdu.packing_service.pojo;


import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotNull;
import javax.validation.groups.Default;
import java.time.LocalDateTime;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class PushTask {

    public interface Update extends Default {}

    public interface Add extends Default{}

    @NotNull(groups = {Task.Update.class})
    private Integer pid; //主键ID

    @NotNull(groups = {Task.Add.class})
    private String orderId; //订单ID

    @NotNull(groups = {Task.Add.class})
    private String type; //类型

    @NotNull(groups = {Task.Add.class})
    private String orderData ; //订单数据地址

    private Integer readStatus; //读取状态

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime pushTime; //推送时间

}
