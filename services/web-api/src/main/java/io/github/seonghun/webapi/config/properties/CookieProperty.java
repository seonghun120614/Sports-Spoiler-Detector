package io.github.seonghun.webapi.config.properties;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "cookie")
public record CookieProperty (
        boolean httpOnly,
        boolean secure,     // Local, Prod: false, https 발급시 true
        String sameSite,    // Local, Prod: Lax, https 발급시 None
        String path
) {}