package cn.edu.hdu.packing_service.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotNull;
import javax.validation.groups.Default;

/**
 * @Author: ZhangWH
 * @Date: 2024/4/7 11:49
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class TruckSpecification {

    public interface Update extends Default {}

    public interface Add extends Default {}

    @NotNull(groups = {Update.class})
    private Integer id;

    @NotNull(groups = {Add.class})
    private String name;

    @NotNull(groups = {Add.class})
    private Double lengthM;

    @NotNull(groups = {Add.class})
    private Double widthM;

    @NotNull(groups = {Add.class})
    private Double heightM;

    @NotNull(groups = {Add.class})
    private Double weightT;
}
