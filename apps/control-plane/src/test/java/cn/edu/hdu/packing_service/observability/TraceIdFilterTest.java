package cn.edu.hdu.packing_service.observability;

import org.junit.jupiter.api.Test;
import org.slf4j.MDC;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;

import javax.servlet.FilterChain;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;

class TraceIdFilterTest {
    @Test
    void propagatesValidTraceIdAndClearsMdc() throws Exception {
        TraceIdFilter filter = new TraceIdFilter();
        MockHttpServletRequest request = new MockHttpServletRequest();
        request.addHeader(TraceIdFilter.HEADER, "trace-12345678");
        MockHttpServletResponse response = new MockHttpServletResponse();
        FilterChain chain = (req, res) -> assertEquals("trace-12345678", MDC.get("traceId"));

        filter.doFilter(request, response, chain);

        assertEquals("trace-12345678", response.getHeader(TraceIdFilter.HEADER));
        assertNull(MDC.get("traceId"));
    }

    @Test
    void replacesMalformedTraceId() throws Exception {
        TraceIdFilter filter = new TraceIdFilter();
        MockHttpServletRequest request = new MockHttpServletRequest();
        request.addHeader(TraceIdFilter.HEADER, "bad value with spaces");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilter(request, response, (req, res) -> { });

        String generated = response.getHeader(TraceIdFilter.HEADER);
        assertEquals(32, generated.length());
        assertFalse(generated.contains(" "));
    }
}
