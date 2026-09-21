# 1단계: 빌드 스테이지 (Gradle과 JDK 21 환경)
FROM gradle:8.5-jdk21 AS builder
WORKDIR /app

# 소스코드 및 설정 파일 복사
COPY gradlew ./
COPY gradle ./gradle
COPY build.gradle settings.gradle ./
COPY src ./src

# 테스트를 제외하고 JAR 파일 빌드 (bootJar)
RUN ./gradlew bootJar --no-daemon -x test

# JAR 를 레이어(dependencies / loader / snapshot / application)별로 분리
RUN cp build/libs/*.jar application.jar \
 && java -Djarmode=tools -jar application.jar extract --layers --destination extracted

# 2단계: 런타임 스테이지 (가벼운 JRE/JDK 21 이미지)
FROM eclipse-temurin:21-jre
WORKDIR /app

# 자주 바뀌지 않는 레이어부터 복사 (배포 시 application 레이어만 새로 push/pull)
COPY --from=builder /app/extracted/dependencies/ ./
COPY --from=builder /app/extracted/spring-boot-loader/ ./
COPY --from=builder /app/extracted/snapshot-dependencies/ ./
COPY --from=builder /app/extracted/application/ ./

# 포트 오픈 및 실행 명령어 설정
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "application.jar"]
