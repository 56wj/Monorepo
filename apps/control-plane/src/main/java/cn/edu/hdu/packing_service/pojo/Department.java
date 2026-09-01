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
 * @Date: 2024/3/18 9:58
 */

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Department {

    @NotNull(groups = {Update.class})
    private Integer departmentId;

    @NotEmpty
    private String departmentName;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;//创建时间

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updateTime;//更新时间

    public interface Add extends Default{}

    public interface Update extends Default{}

    public interface Delete extends Default{}
}
