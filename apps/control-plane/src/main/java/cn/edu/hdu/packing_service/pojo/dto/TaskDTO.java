package cn.edu.hdu.packing_service.pojo.dto;

import cn.edu.hdu.packing_service.pojo.Task;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import java.time.LocalDateTime;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/12 16:04
 */

@NoArgsConstructor
@AllArgsConstructor
@Data
public class TaskDTO {

    @NotNull(groups = {Task.Update.class})
    private Integer id;

    @NotNull(groups = {Task.Add.class})
    private String orderId; //订单ID

    private String sourceJson;

    @NotNull(groups = {Task.Update.class})
    private String type;

    @NotNull(groups = {Task.Update.class})
    private String state;

    private Integer createUser;

    private String userName;

    private String resultJson;

    private String middleJosn;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updateTime;

}
