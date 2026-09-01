package cn.edu.hdu.packing_service.Annotation;


import java.lang.annotation.*;

@Documented //这个其实个人感觉没啥用，主要是在javadoc上生成注解用的
@Target(ElementType.METHOD)//注解放置的目标位置,METHOD是可注解在方法级别上
/**
 * 　　　　1.CONSTRUCTOR:用于描述构造器
 * 　　　　2.FIELD:用于描述域
 * 　　　　3.LOCAL_VARIABLE:用于描述局部变量
 * 　　　　4.METHOD:用于描述方法
 * 　　　　5.PACKAGE:用于描述包
 * 　　　　6.PARAMETER:用于描述参数
 * 　　　　7.TYPE:用于描述类、接口(包括注解类型) 或enum声明
 * **/
@Retention(RetentionPolicy.RUNTIME)
/**
 * 1、RetentionPolicy.SOURCE：注解只保留在源文件，当Java文件编译成class文件的时候，注解被遗弃；
 * 2、RetentionPolicy.CLASS：注解被保留到class文件，但jvm加载class文件时候被遗弃，这是默认的生命周期；
 * 3、RetentionPolicy.RUNTIME：注解不仅被保存到class文件中，jvm加载class文件之后，仍然存在；
 * 首先要明确生命周期长度SOURCE < CLASS < RUNTIME ，所以前者能作用的地方后者一定也能作用。一般如果需要在运行时去动态获取注解信息，
 * 那只能用RUNTIME 注解；如果要在编译时进行一些预处理操作，比如生成一些辅助代码（如ButterKnife），就用CLASS注解；如果只是做一些检查性的操作，
 * 比如@Override 和@SuppressWarnings，则可选用SOURCE 注解。
 * **/
public @interface MyAnnotation {
    String moudle() default ""; //模块
    String operate() default ""; //操作
}
