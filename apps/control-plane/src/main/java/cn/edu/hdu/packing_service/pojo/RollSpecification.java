package cn.edu.hdu.packing_service.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import javax.validation.groups.Default;
import java.util.Objects;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class RollSpecification {

    public interface Update extends Default {}

    public interface Add extends Default {}

    @NotNull(groups = {Update.class})
    private Integer id;

    @NotEmpty
    private String rollName;

    @NotNull
    private Double rollThickness;

    @NotNull
    private Double rollLength;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        RollSpecification that = (RollSpecification) o;
        return Objects.equals(rollThickness, that.rollThickness) && Objects.equals(rollLength, that.rollLength);
    }

    @Override
    public int hashCode() {
        return Objects.hash(rollThickness, rollLength);
    }
}
