package io.github.seonghun.webapi.controller;

import io.github.seonghun.webapi.service.JwtTokenService;
import io.github.seonghun.webapi.common.util.CookieHandler;
import io.github.seonghun.webapi.common.util.JwtProvider;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import static org.springframework.http.HttpHeaders.SET_COOKIE;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class AuthenticationController {
    private final JwtProvider jwtProvider;
    private final CookieHandler cookieHandler;
    private final JwtTokenService jwtTokenService;

    @PostMapping("/logout")
    public ResponseEntity<Void> logout(@CookieValue("refresh_token") String refreshToken,
                                       HttpServletResponse response) {
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
}
