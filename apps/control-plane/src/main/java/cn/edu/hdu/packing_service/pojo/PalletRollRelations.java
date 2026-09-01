package cn.edu.hdu.packing_service.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotNull;
import javax.validation.groups.Default;
import java.util.Objects;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PalletRollRelations {

    public interface Update extends Default {}

    public interface Add extends Default {}


    @NotNull
    private Integer palletId;

    @NotNull
    private Integer rollId;

    @NotNull
    private Integer rollNums;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PalletRollRelations that = (PalletRollRelations) o;
        return Objects.equals(palletId, that.palletId) && Objects.equals(rollId, that.rollId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(palletId, rollId);
    }
}
