package cn.edu.hdu.packing_service.pojo;



import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import javax.validation.groups.Default;
import java.time.LocalDateTime;
import java.util.List;

/**
 * 用户实体类
 */
//
//使用lombok注解，自动生成getter setter toString 方法
@Data
public class User {

    public interface Update extends Default {}

    public interface Add extends Default{}

    public interface AdminUpdate extends Default{}

    @NotNull(groups = {AdminUpdate.class})
    private Integer id;//主键ID

    @NotEmpty
    private String username;//用户名


    private String password;//密码

    @JsonIgnore
    public String getPassword() {
        return password;
    }

    @JsonProperty
    public void setPassword(String password) {
        this.password = password;
    }


    @NotEmpty(groups = {Add.class})
    private String roles; //角色

    private List<String> rolesList; //角色列表

    @NotEmpty(groups = {Add.class,AdminUpdate.class})
    private String department;//部门

    @NotEmpty(groups = {Update.class})
    @Email(groups = {Update.class})
    private String email;//邮箱

    @NotEmpty(groups = {Update.class})
    @Pattern(regexp = "^1[3|4|5|7|8][0-9]\\d{8}$" , groups = {Update.class})
    private String phone; //电话

    private String avatar;//用户头像地址

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;//创建时间

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updateTime;//更新时间

}
