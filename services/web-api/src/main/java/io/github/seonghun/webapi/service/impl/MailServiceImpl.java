package io.github.seonghun.webapi.service.impl;

import io.github.seonghun.webapi.common.util.CustomMailSender;
import io.github.seonghun.webapi.common.util.RandomGenerator;
import io.github.seonghun.webapi.common.util.RedisUtil;
import io.github.seonghun.webapi.service.MailService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;


@Service
@RequiredArgsConstructor
public class MailServiceImpl implements MailService {

    private final RedisUtil redisUtil;
    private final CustomMailSender mailSender;
    private final RandomGenerator randomGenerator;

    private static final String VERIFICATION_SUBJECT = "[Sport Spoiler Detector] 이메일 인증 코드 발송 안내";
    private static final String VERIFICATION_BODY_TEMPLATE = """
            <div style="font-family: 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; max-width: 600px; margin: 0 auto; padding: 40px 20px; text-align: center; border: 1px solid #eaeaea; border-radius: 10px;">
                <h2 style="color: #333; margin-bottom: 20px;">이메일 인증 코드</h2>
                <p style="color: #666; font-size: 15px; line-height: 1.6; margin-bottom: 30px;">
                    Sport Spoiler Detector 서비스에 가입해 주셔서 감사합니다.<br>
                    아래의 6자리 인증 코드를 진행 중인 화면에 입력해 주세요.
                </p>
                <div style="background-color: #f4f6f8; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
                    <span style="font-size: 28px; font-weight: bold; color: #0056b3; letter-spacing: 10px;">
                        %s
                    </span>
                </div>
                <p style="color: #999; font-size: 12px;">
                    본 코드는 5분간 유효합니다.<br>
                    본인이 요청하지 않으셨다면 이 메일을 무시해 주세요.
                </p>
            </div>
            """;

    @Override
    public void sendVerificationMail(String email) {
        if (redisUtil.get("mail-verification", email) != null)
            throw new IllegalStateException("You have already been issued a code. Please try again in a moment.");
        var code = randomGenerator.generateAlphanumeric(6);
        String mailBody = String.format(VERIFICATION_BODY_TEMPLATE, code);
        mailSender.sendEmail(email, VERIFICATION_SUBJECT, mailBody);
        redisUtil.save("mail-verification", email, code, 60_000);
    }

    @Override
    public boolean verifyMailCode(String email, String code) {
        var checked = redisUtil.isValidAndEquals("mail-verification", email, code);
        if (checked)
            redisUtil.save("mail-verification", email, "complete", 600_000);
        return checked;
    }
}