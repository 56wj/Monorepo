package cn.edu.hdu.packing_service.job;

import lombok.Data;

@Data
public class JobStatusCount {
    private String status;
    private Long count;
}
