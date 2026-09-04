package io.github.seonghun.webapi.config.properties;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "jwt")
public record JwtProperty(
        String secret,
        long accessExpireMilliSeconds,
        long refreshExpireMilliSeconds
) {}