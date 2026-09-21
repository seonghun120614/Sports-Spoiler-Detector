package io.github.seonghun.webapi.controller;

import io.github.seonghun.webapi.client.LlmWorkerClient;
import io.github.seonghun.webapi.client.dto.CheckSpoilerRequest;
import io.github.seonghun.webapi.client.dto.CheckSpoilerResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/spoiler")
public class SpoilerController {

    private final LlmWorkerClient llmWorkerClient;

    @PostMapping
    public ResponseEntity<List<CheckSpoilerResponse>> check(@RequestBody List<@Valid CheckSpoilerRequest> request) {
        return ResponseEntity.ok(llmWorkerClient.checkSpoiler(request));
    }
}
