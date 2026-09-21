package io.github.seonghun.webapi.client.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public record CheckSpoilerResponse(

        @JsonProperty("video_id") String videoId,
        String title,
        int width,
        int height,
        String spoiler,
        List<TextSpoiler> texts,
        List<ImageSpoiler> images
) {

    // frozen=True 대응: 외부에서 리스트를 바꿀 수 없게 불변 복사
    public CheckSpoilerResponse {
        texts = List.copyOf(texts);
        images = List.copyOf(images);
    }

    public int totalSpoilerCount() {
        return texts.size() + images.size();
    }

    // ---- 공통 인터페이스 (SpoilerElement) ----
    public interface SpoilerElement {
        String label();       // nullable
        double confidence();
    }

    // ---- 좌표 ----
    public record Point(double x, double y) {

        public Point scaling(double multiplierX, double multiplierY) {
            return new Point(x * multiplierX, y * multiplierY);
        }

        public Point withX(double x) {
            return new Point(x, y);
        }

        public Point withY(double y) {
            return new Point(x, y);
        }
    }

    public record BoundingBox(
            @JsonProperty("top_left") Point topLeft,
            @JsonProperty("bottom_right") Point bottomRight
    ) {
        public double[] xyxy() {
            return new double[]{topLeft.x(), topLeft.y(), bottomRight.x(), bottomRight.y()};
        }
    }

    // ---- 텍스트 스포일러 ----
    public record TextSpan(int start, int end) {}

    public record TextSpoiler(
            String label,
            double confidence,
            String text,
            TextSpan span
    ) implements SpoilerElement {

        public static TextSpoiler of(SpoilerElement elem, TextSpan span, String text) {
            return new TextSpoiler(elem.label(), elem.confidence(), text, span);
        }
    }

    // ---- 이미지 스포일러 ----
    public record ImageSpoiler(
            String label,
            double confidence,
            @JsonProperty("bounding_box") BoundingBox boundingBox
    ) implements SpoilerElement {

        public static ImageSpoiler of(SpoilerElement elem, BoundingBox boundingBox) {
            return new ImageSpoiler(elem.label(), elem.confidence(), boundingBox);
        }

        public ImageSpoiler withLabel(String label) {
            return new ImageSpoiler(label, confidence, boundingBox);
        }

        // 파이썬의 set_confidence: 값을 대입하는 게 아니라 기존 confidence에 곱함
        public ImageSpoiler scaleConfidence(double factor) {
            double scaled = Math.round(confidence * factor * 100) / 100.0;
            return new ImageSpoiler(label, scaled, boundingBox);
        }
    }
}