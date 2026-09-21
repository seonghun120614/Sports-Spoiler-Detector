FROM gradle:8.5-jdk21 AS builder
WORKDIR /app

# 1) 빌드 스크립트만 먼저 → 의존성 해결을 별도 레이어로
COPY gradlew ./
COPY gradle ./gradle
COPY build.gradle settings.gradle ./
RUN --mount=type=cache,target=/home/gradle/.gradle \
    ./gradlew dependencies --no-daemon || true

# 2) 그 다음 소스
COPY src ./src
RUN --mount=type=cache,target=/home/gradle/.gradle \
    ./gradlew bootJar --no-daemon -x test

RUN cp build/libs/*.jar application.jar \
 && java -Djarmode=tools -jar application.jar extract --layers --destination extracted

FROM eclipse-temurin:21-jre
WORKDIR /app

# 3) 각자 다른 경로로 → 레이어가 실제로 분리됨
COPY --from=builder /app/extracted/dependencies/ ./
COPY --from=builder /app/extracted/spring-boot-loader/ ./
COPY --from=builder /app/extracted/snapshot-dependencies/ ./
COPY --from=builder /app/extracted/application/ ./

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "application.jar"]