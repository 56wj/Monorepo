package cn.edu.hdu.packing_service.utils;

import java.util.Map;

/**
 * 托盘装箱跨入口的最小业务校验。
 *
 * 膜叠膜的两个高度配置单位均为cm，并且在开启膜叠膜时必填。
 * 这里在创建异步任务之前拦截错误，避免Python子进程异常后页面一直显示“计算中”。
 */
public final class PalletPackingConfigValidator {

    private PalletPackingConfigValidator() {
    }

    public static String validateRequest(Map<String, ?> request) {
        if (request == null || !(request.get("data") instanceof Map)) {
            return "请求缺少装箱数据data";
        }
        return validateData((Map<?, ?>) request.get("data"));
    }

    public static String validateData(Map<?, ?> data) {
        if (data == null || !(data.get("config") instanceof Map)) {
            return "请求缺少装箱规则config";
        }

        Map<?, ?> config = (Map<?, ?>) data.get("config");
        if (!isEnabled(config.get("overlap"))) {
            return null;
        }

        String error = validatePositiveHeight(config.get("single_max_height"), "单层膜卷本体高度上限");
        if (error != null) {
            return error;
        }
        return validatePositiveHeight(config.get("entire_max_height"), "叠后膜卷本体总高度上限");
    }

    private static boolean isEnabled(Object value) {
        return Boolean.TRUE.equals(value) || "true".equalsIgnoreCase(String.valueOf(value));
    }

    private static String validatePositiveHeight(Object value, String label) {
        if (value == null || String.valueOf(value).trim().isEmpty()) {
            return "开启膜叠膜时必须填写" + label + "(cm)";
        }

        try {
            double height = Double.parseDouble(String.valueOf(value));
            if (!Double.isFinite(height) || height <= 0) {
                return label + "必须是大于0的数字，单位cm";
            }
        } catch (NumberFormatException exception) {
            return label + "必须是大于0的数字，单位cm";
        }
        return null;
    }
}
