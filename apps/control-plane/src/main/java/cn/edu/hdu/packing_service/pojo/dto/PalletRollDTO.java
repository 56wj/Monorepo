package cn.edu.hdu.packing_service.pojo.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PalletRollDTO {

    private Integer palletId;

    private Integer rollId;

    private Integer rollNums;

    private String palletName;

    private Double palletLength;

    private Double palletWidth;

    private Double palletHeight;

    private Double palletWeight;

    private String palletType;

    private String palletRemark;

    private Double rollThickness;

    private Double rollLength;

}
