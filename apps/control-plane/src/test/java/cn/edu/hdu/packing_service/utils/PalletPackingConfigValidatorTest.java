package cn.edu.hdu.packing_service.utils;

import cn.edu.hdu.packing_service.controller.PalletPackingController;
import cn.edu.hdu.packing_service.pojo.Result;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PalletPackingConfigValidatorTest {

    @Test
    void requiresBothHeightsWhenOverlapIsEnabled() {
        Map<String, Object> config = new HashMap<>();
        config.put("overlap", true);
        config.put("single_max_height", "");
        config.put("entire_max_height", null);

        String error = PalletPackingConfigValidator.validateData(dataWith(config));

        assertTrue(error.contains("单层"));
    }

    @Test
    void rejectsMissingTotalHeight() {
        Map<String, Object> config = new HashMap<>();
        config.put("overlap", true);
        config.put("single_max_height", 70);
        config.put("entire_max_height", "");

        String error = PalletPackingConfigValidator.validateData(dataWith(config));

        assertTrue(error.contains("总高度"));
    }

    @Test
    void acceptsPositiveCentimeterLimits() {
        Map<String, Object> config = new HashMap<>();
        config.put("overlap", true);
        config.put("single_max_height", 70);
        config.put("entire_max_height", 140.5);

        assertNull(PalletPackingConfigValidator.validateData(dataWith(config)));
    }

    @Test
    void doesNotRequireLimitsWhenOverlapIsDisabled() {
        Map<String, Object> config = new HashMap<>();
        config.put("overlap", false);

        assertNull(PalletPackingConfigValidator.validateData(dataWith(config)));
    }

    @Test
    void controllerRejectsMissingLimitsBeforeCreatingTask() {
        Map<String, Object> config = new HashMap<>();
        config.put("overlap", true);
        config.put("single_max_height", 70);
        config.put("entire_max_height", "");

        Map<String, Object> request = new HashMap<>();
        request.put("orderID", "TEST-OVERLAP-VALIDATION");
        request.put("data", dataWith(config));

        Result result = new PalletPackingController().computerFirst(request);

        assertEquals(0, result.getCode());
        assertTrue(result.getMessage().contains("总高度"));
    }

    private Map<String, Object> dataWith(Map<String, Object> config) {
        Map<String, Object> data = new HashMap<>();
        data.put("config", config);
        return data;
    }
}
