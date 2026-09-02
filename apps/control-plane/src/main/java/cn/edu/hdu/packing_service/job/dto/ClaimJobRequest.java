package cn.edu.hdu.packing_service.job.dto;

import lombok.Data;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import java.util.List;

@Data
public class ClaimJobRequest {
    @NotEmpty
    private String workerId;

    @NotEmpty
    private List<String> capabilities;

    @NotNull
    private Integer leaseSeconds;
}
