package cn.edu.hdu.packing_service.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotNull;
import javax.validation.groups.Default;
import java.util.Objects;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/18 11:07
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class PalletSpecification {

    public interface Update extends Default {}

    public interface Add extends Default {}

    @NotNull(groups = {Update.class})
    private Integer id;

    @NotNull
    private String palletName;

    @NotNull
    private Double palletLength;

    @NotNull Double palletWidth;

    @NotNull
    private Double palletHeight;

    @NotNull
    private Double palletWeight;

    @NotNull
    private String palletType;


    private String palletRemark;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PalletSpecification that = (PalletSpecification) o;
        return Objects.equals(palletLength, that.palletLength) && Objects.equals(palletWidth, that.palletWidth) && Objects.equals(palletHeight, that.palletHeight) && Objects.equals(palletWeight, that.palletWeight) && Objects.equals(palletType, that.palletType);
    }

    @Override
    public int hashCode() {
        return Objects.hash(palletLength, palletWidth, palletHeight, palletWeight, palletType);
    }
}
