package io.github.seonghun.webapi.controller;

import io.github.seonghun.webapi.service.JwtTokenService;
import io.github.seonghun.webapi.common.util.CookieHandler;
import io.github.seonghun.webapi.common.util.JwtProvider;
import io.github.seonghun.webapi.service.MailService;
import io.github.seonghun.webapi.service.UserService;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import static org.springframework.http.HttpHeaders.SET_COOKIE;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthenticationController {

    private final UserService userService;
    private final JwtProvider jwtProvider;
    private final CookieHandler cookieHandler;
    private final JwtTokenService jwtTokenService;
    private final MailService mailService;

    @PostMapping("/verification/send-mail")
    public ResponseEntity<Void> sendVerificationMail(@RequestBody SendMailRequest request) {
        if (userService.exists(request.email()))
            throw new IllegalArgumentException("User with email " + request.email() + " already exists");

        mailService.sendVerificationMail(request.email());

        return ResponseEntity.noContent().build();
    }

    @PostMapping("/verification/mail")
    public ResponseEntity<Boolean> verifyMail(
            @Valid @RequestBody VerifyMailRequest request
    ) {
        var checked = mailService.verifyMailCode(request.email(), request.code());

        return ResponseEntity.ok(checked);
    }

    @PostMapping("/logout")
    public ResponseEntity<Void> logout(
            @CookieValue(defaultValue = "", required = false) String refreshToken,
            HttpServletResponse response
    ) {
        if (refreshToken != null) {
            try {
                Claims claims = jwtProvider.parse(refreshToken);
                long remainingMillis = claims.getExpiration().getTime() - System.currentTimeMillis();
                jwtTokenService.blacklist(claims.getId(), remainingMillis);
            } catch (JwtException | IllegalArgumentException ignored) { }
        }

        response.addHeader(SET_COOKIE, cookieHandler.createCookie("access_token", "", 0).toString());
        response.addHeader(SET_COOKIE, cookieHandler.createCookie("refresh_token", "", 0).toString());

        return ResponseEntity.noContent().build();
    }

    public record SendMailRequest(
            @NotBlank(message = "이메일은 필수입니다.")
            @Email(message = "이메일 형식이 올바르지 않습니다.")
            String email
    ) {}

    public record VerifyMailRequest(
            @NotBlank(message = "이메일은 필수입니다.")
            @Email(message = "이메일 형식이 올바르지 않습니다.")
            String email,

            @NotBlank(message = "인증 코드는 필수입니다.")
            String code
    ) {}
}
