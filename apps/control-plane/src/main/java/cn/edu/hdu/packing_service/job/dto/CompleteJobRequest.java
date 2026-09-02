package cn.edu.hdu.packing_service.job.dto;

import com.fasterxml.jackson.databind.JsonNode;
import lombok.Data;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

@Data
public class CompleteJobRequest {
    @NotEmpty
    private String leaseToken;

    @NotNull
    private JsonNode output;
}
