package cn.edu.hdu.packing_service.pojo;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.groups.Default;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TubeSpecification {

    public interface Update extends Default {}

    public interface Add extends Default {}

    @NotNull(groups = {RollSpecification.Update.class})
    private Integer id;

    @NotEmpty
    private String tubeName;

    @NotNull
    private Double tubeApproximate;

    //包含近似值和名称
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        TubeSpecification that = (TubeSpecification) o;
        return tubeApproximate.equals(that.tubeApproximate) && tubeName.equals(that.tubeName);
    }

    //包含近似值和名称
    @Override
    public int hashCode() {
        return tubeApproximate.hashCode() + tubeName.hashCode();
    }

}
