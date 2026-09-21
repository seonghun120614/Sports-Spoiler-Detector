package io.github.seonghun.webapi.client;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.github.seonghun.webapi.client.dto.CheckSpoilerRequest;
import io.github.seonghun.webapi.client.dto.CheckSpoilerResponse;
import io.github.seonghun.webapi.config.properties.LlmWorkerProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.http.MediaType;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

import java.util.List;
import java.util.Map;

@Component
@EnableConfigurationProperties(LlmWorkerProperty.class)
public class LlmWorkerClient {

    private final RestClient restClient;

    public LlmWorkerClient(LlmWorkerProperty property) {
        var requestFactory = new SimpleClientHttpRequestFactory();
        requestFactory.setConnectTimeout(property.connectTimeout());
        requestFactory.setReadTimeout(property.readTimeout());

        this.restClient = RestClient.builder()
                .baseUrl(property.baseUrl())
                .requestFactory(requestFactory)
                .build();
    }

    public List<CheckSpoilerResponse> checkSpoiler(List<CheckSpoilerRequest> request) {
        // llm-worker 는 빈 배열이 오면 response_model 과 다른 [] 를 반환하므로 호출하지 않음
        if (request.isEmpty()) {
            return List.of();
        }

        CheckSpoilerEnvelope envelope = restClient.post()
                .uri("/v1/check-spoiler")
                .contentType(MediaType.APPLICATION_JSON)
                .body(request)
                .retrieve()
                .body(CheckSpoilerEnvelope.class);

        return List.copyOf(envelope.spoilerInformation().values());
    }

    // llm-worker 응답: { "spoiler_information": { "<video_id>": {...} }, "api_version": ..., "timestamp": ... }
    private record CheckSpoilerEnvelope(
            @JsonProperty("spoiler_information") Map<String, CheckSpoilerResponse> spoilerInformation
    ) {}
}
