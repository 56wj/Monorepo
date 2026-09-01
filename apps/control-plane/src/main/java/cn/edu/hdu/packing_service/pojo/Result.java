package cn.edu.hdu.packing_service.pojo;

import cn.edu.hdu.packing_service.constant.StatusCodes;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @Author: ZhangWH
 * @Date: 2024/2/28 11:17
 */
//统一响应结果

@NoArgsConstructor
@AllArgsConstructor
@Data
public class Result<T> {
    private Integer code;//业务状态码  0-成功  1-失败
    private String message;//提示信息
    private T data;//响应数据

    //快速返回操作成功响应结果(带响应数据)
    public static <E> Result<E> success(E data) {
        return new Result<>(StatusCodes.NORMAL_SUCCESS_CODE, "操作成功", data);
    }

    //快速返回操作成功响应结果
    public static Result success() {
        return new Result(StatusCodes.NORMAL_SUCCESS_CODE, "操作成功", null);
    }

    //自定义返回操作成功响应结果
    public static <E> Result<E> success(Integer code , String message, E data) {
        return new Result<>(code, message, data);
    }

    //快速返回操作失败响应结果
    public static Result error(String message) {
        return new Result(0, message, null);
    }

    //自定义返回操作失败响应结果
    public static Result error(Integer code , String message) {
        return new Result(code, message, null);
    }

}
