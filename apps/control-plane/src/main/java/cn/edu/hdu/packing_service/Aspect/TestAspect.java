package cn.edu.hdu.packing_service.Aspect;

import cn.edu.hdu.packing_service.Annotation.MyAnnotation;
import com.alibaba.fastjson.JSON;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.stereotype.Component;

import java.lang.reflect.Method;

@Aspect
@Component
@Slf4j
public class TestAspect {
    /**
     * 设置操作日志切入点 记录操作日志 在注解的位置切入代码
     *     @Pointcut("execution(* com.crud.controller.BlogController.getBlogById())")
     *     上面的这种是excution表达式，比如说我并不想开发一个专门的注解，我就想在某一个或者某一类的方法上添加这个aop，那就可以通过excution表达式来做
     * @Pointcut("execution(public * com.crud.controller.*.*(..))")
     * ..两个点表明多个，*代表一个， 上面表达式代表切入com.xhx.springboot.controller包下的所有类的所有方法，
     * 方法参数不限，返回类型不限。 其中访问修饰符可以不写，不能用*，，第一个*代表返回类型不限，第二个*表示所有类，第三个*表示所有方法，..两个点表示方法里的参数不限
     * 有一点非常重要，Spring的AOP只能支持到方法级别的切入。换句话说，切入点只能是某个方法
     */
    // 定义切入点
    @Pointcut("@annotation(cn.edu.hdu.packing_service.Annotation.MyAnnotation)")
    public void logAspectPoint(){}

    @Pointcut("execution(* cn.edu.hdu.packing_service.service.*.*(..))")
    public void logMethod(){}

    @Around("logAspectPoint()")
    public Object log(ProceedingJoinPoint proceedingJoinPoint) throws Throwable {
        //前置
        long startTime= System.currentTimeMillis();
        /**
         * 环绕通知=前置+目标方法执行+后置，proceed方法就是用于启动目标方法执行的
         * Proceedingjoinpoint 继承了 JoinPoint。是在JoinPoint的基础上暴露出 proceed 这个方法。proceed很重要，这个是aop代理链执行的方法。
         * 暴露出这个方法，就能支持 aop:around 这种切面（而其他的几种切面只需要用到JoinPoint，，这也是环绕通知和前置、后置通知方法的一个最大区别。这跟切面类型有关）
         * */
        Object result=proceedingJoinPoint.proceed();
        //后置
        long time=System.currentTimeMillis()-startTime;
        recordLog(proceedingJoinPoint,time);
        return result;
    }


    @Around("logMethod()")
    public Object Methlod(ProceedingJoinPoint proceedingJoinPoint) throws Throwable {

        long startTime= System.currentTimeMillis();

        Object result=proceedingJoinPoint.proceed();
        //后置
        long time=System.currentTimeMillis()-startTime;
        recordLog(proceedingJoinPoint,time);
        return result;
    }


    public void recordLog(ProceedingJoinPoint proceedingJoinPoint,long time){
        //getSignature());是获取到这样的信息 :修饰符+ 包名+组件名(类名) +方法名
        MethodSignature methodSignature= (MethodSignature) proceedingJoinPoint.getSignature();
        Method method=methodSignature.getMethod();
        //getAnnotation:方法如果存在这样的注释，则返回指定类型的元素的注释，否则为null
        MyAnnotation logAnnotation=method.getAnnotation(MyAnnotation.class);
        log.info("==============================开始记录日志===============================");
        if (logAnnotation != null) {
            log.info("moudle:{}", logAnnotation.moudle());
            log.info("operato:{}", logAnnotation.operate());
        }
        //proceedingJoinPoint.getTarget():获取切入点所在目标对象
        String className=proceedingJoinPoint.getTarget().getClass().getName();
        String methodName=methodSignature.getName();
        log.info("请求的方法是：{}",className+"."+methodName+"()");
        //这里返回的是切入点方法的参数列表
        Object[] args=proceedingJoinPoint.getArgs();
        StringBuilder sb = new StringBuilder();
        for (Object o : args){
             sb.append(JSON.toJSONString(o)).append(" ");

        }
        log.info("请求的参数是:{}",sb);
        log.info("执行时间总共为:{}",time);
        log.info("=================================end===================================");
    }
}