package cn.edu.hdu.packing_service.job.dto;

import lombok.Data;

import javax.validation.constraints.NotEmpty;

@Data
public class LeaseRequest {
    @NotEmpty
    private String leaseToken;
}
