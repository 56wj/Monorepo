package cn.edu.hdu.packing_service.job.dto;

import lombok.Data;

import javax.validation.constraints.NotEmpty;

@Data
public class FailJobRequest {
    @NotEmpty
    private String leaseToken;
    private String errorCode;
    private String errorMessage;
    private boolean retryable = true;
}
