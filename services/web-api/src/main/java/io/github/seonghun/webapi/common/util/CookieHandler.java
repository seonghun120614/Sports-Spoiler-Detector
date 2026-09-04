package io.github.seonghun.webapi.common.util;

import io.github.seonghun.webapi.config.properties.CookieProperty;
import jakarta.servlet.http.Cookie;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseCookie;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.stream.Collectors;

@Component
@RequiredArgsConstructor
public class CookieHandler {
    private final CookieProperty cookieProperty;

    public ResponseCookie createCookie(String name, String value, long maxAge) {
        return ResponseCookie.from(name, value)
                             .httpOnly(cookieProperty.httpOnly())
                             .secure(cookieProperty.secure())
                             .sameSite(cookieProperty.sameSite())
                             .path(cookieProperty.path())
                             .maxAge(maxAge)
                             .build();
    }

    public Map<String, String> getMap(Cookie[] cookies) {
        if (cookies == null || cookies.length == 0)
            return Collections.EMPTY_MAP;
        return Arrays.stream(cookies)
                     .collect(Collectors.toMap(Cookie::getName, Cookie::getValue));
    }
}
