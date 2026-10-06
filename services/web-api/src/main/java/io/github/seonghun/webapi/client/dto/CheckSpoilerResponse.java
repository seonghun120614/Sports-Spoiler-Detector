package io.github.seonghun.webapi.client.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public record CheckSpoilerResponse(
        @JsonProperty("video_id") String videoId,
        String title,
        int width,
        int height,
        List<TextEntity> texts,
        List<ImageRegion> images
) {
    public record TextEntity(String label, double confidence, String text, Span span) {}

    public record Span(int start, int end) {}

    public record ImageRegion(
            String label,
            double confidence,
            @JsonProperty("bounding_box") BoundingBox boundingBox
    ) {}

    public record BoundingBox(
            @JsonProperty("top_left") Point topLeft,
            @JsonProperty("bottom_right") Point bottomRight
    ) {}

    public record Point(double x, double y) {}
}