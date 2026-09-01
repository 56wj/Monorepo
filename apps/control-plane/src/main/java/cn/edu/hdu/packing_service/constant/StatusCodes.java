package cn.edu.hdu.packing_service.constant;

/**
 * @Author: ZhangWH
 * @Date: 2024/4/10 14:09
 */
public final class StatusCodes {
    public static final int NORMAL_SUCCESS_CODE = 20000;
    public static final int PALLET_FIRST_CODE = 10001;
    public static final int PALLET_SECOND_CODE = 10002;
    public static final int SUSPEND_FIRST_CODE = 20001;



    //文件地址错误
    public static final int FILE_PATH_ERROR = 90001;

    //文件读取错误
    public static final int FILE_READ_ERROR = 90002;

    //文件写入错误
    public static final int FILE_WRITE_ERROR = 90003;

    //文件删除错误
    public static final int FILE_DELETE_ERROR = 90004;

    //任务为空错误
    public static final int TASK_NULL_ERROR = 90005;

    private StatusCodes() {
    }
}
