package io.github.seonghun.webapi.client.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public record CheckSpoilerRequest(
        @JsonProperty("video_id")
        @NotNull(message = "video_id is required")
        @Pattern(
                regexp = "[a-zA-Z0-9_-]{11}",
                message = "Video ID, it must be 11 characters long"
        )
        String videoId,

        @NotEmpty(message = "Video title, it must not be empty")
        String title
) {}