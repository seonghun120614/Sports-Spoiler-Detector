package io.github.seonghun.webapi.security.jwt;

import io.github.seonghun.webapi.service.JwtTokenService;
import io.github.seonghun.webapi.common.util.CookieHandler;
import io.github.seonghun.webapi.common.util.JwtProvider;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

@Component
@RequiredArgsConstructor
public class JwtRefreshFilter extends OncePerRequestFilter {
    private final static String INCLUDE_PATHS = "/api/refresh";

    private final JwtTokenService jwtTokenService;
    private final CookieHandler cookieHandler;
    private final JwtProvider jwtProvider;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain
    ) throws IOException {
        // Parsing
        Map<String, String> tokens = cookieHandler.getMap(request.getCookies());

        try {
            String oldRefreshToken = tokens.getOrDefault("refresh_token", "");
            Claims oldRefreshClaim = jwtProvider.parse(oldRefreshToken);

            if (jwtTokenService.isBlacklisted(oldRefreshClaim.getId())) {
                response.setStatus(HttpStatus.UNAUTHORIZED.value());
                response.setContentType(MediaType.APPLICATION_JSON_VALUE);
                response.setCharacterEncoding(StandardCharsets.UTF_8.name());
                response.getWriter().write("무효화된 토큰");
            }

            String jti = oldRefreshClaim.getId();
            String uid = oldRefreshClaim.getSubject();

            @SuppressWarnings("unchecked")
            List<String> roleList = oldRefreshClaim.get("roles", List.class);
            Set<String> authorities = new HashSet<>(roleList);

            // 만들기 전 jti black
            var remainingMillis = oldRefreshClaim.getExpiration().getTime() - System.currentTimeMillis();
            jwtTokenService.blacklist(jti, remainingMillis);

            // 새 Access Token 발행
            String accessToken = jwtProvider.createAccessToken(uid, authorities);
            String[] jtiRefreshToken = jwtProvider.createRefreshToken(uid, authorities);

            jwtTokenService.cache(uid, jtiRefreshToken[0]);
            var accessCookie = cookieHandler.createCookie("access_token",
                                                          accessToken,
                                                          jwtProvider.getAccessExpirySeconds());
            var refreshCookie = cookieHandler.createCookie("refresh_token",
                                                           jtiRefreshToken[1],
                                                           jwtProvider.getRefreshExpirySeconds());

            response.addHeader(HttpHeaders.SET_COOKIE, accessCookie.toString());
            response.addHeader(HttpHeaders.SET_COOKIE, refreshCookie.toString());
            response.setStatus(HttpServletResponse.SC_NO_CONTENT);
        } catch (JwtException | IllegalArgumentException e) {
            response.setStatus(HttpStatus.UNAUTHORIZED.value());
            response.setContentType(MediaType.APPLICATION_JSON_VALUE);
            response.setCharacterEncoding(StandardCharsets.UTF_8.name());
            response.getWriter().write("잘못된 형식");
        }
    }

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        return !INCLUDE_PATHS.equals(request.getRequestURI());
    }
}
