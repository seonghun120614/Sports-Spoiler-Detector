package io.github.seonghun.webapi.common.util;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class CustomMailSender {

    private final JavaMailSender javaMailSender;

    /**
     * 이메일 전송 (HTML 포맷 지원)
     *
     * @param to      수신자 이메일 주소
     * @param subject 이메일 제목
     * @param content 이메일 본문 (HTML 태그 사용 가능)
     */
    public void sendEmail(String to, String subject, String content) {
        try {
            // MimeMessage: 텍스트뿐만 아니라 HTML, 첨부파일 등을 지원하는 다목적 메세지 객체
            MimeMessage message = javaMailSender.createMimeMessage();

            // Helper의 두 번째 인자(false)는 멀티파트(첨부파일) 미사용, 세 번째 인자는 인코딩 설정
            MimeMessageHelper helper = new MimeMessageHelper(message, false, "UTF-8");

            helper.setTo(to);
            helper.setSubject(subject);
            // 두 번째 인자(true)를 통해 HTML 렌더링 활성화
            helper.setText(content, true);

            javaMailSender.send(message);
            log.info("메일 전송 성공 - 수신자: {}", to);

        } catch (MessagingException e) {
            log.error("메일 전송 실패 - 수신자: {}, 원인: {}", to, e.getMessage());
            throw new RuntimeException("이메일 전송 중 오류가 발생했습니다.", e);
        }
    }
}