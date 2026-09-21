package io.github.seonghun.webapi.config.properties;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.time.Duration;

@ConfigurationProperties(prefix = "llm-worker")
public record LlmWorkerProperty(
        String baseUrl,
        Duration connectTimeout,
        Duration readTimeout
) {}
