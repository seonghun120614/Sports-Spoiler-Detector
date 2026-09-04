package io.github.seonghun.webapi.security.userpwd;

import io.github.seonghun.webapi.service.JwtTokenService;
import io.github.seonghun.webapi.common.util.CookieHandler;
import io.github.seonghun.webapi.common.util.JwtProvider;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;

import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

@RequiredArgsConstructor
public class UsernamePasswordAuthenticationSuccessHandler
        implements AuthenticationSuccessHandler {

    private final JwtTokenService jwtTokenService;
    private final JwtProvider jwtProvider;
    private final CookieHandler cookieHandler;

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
                                        HttpServletResponse response,
                                        Authentication authentication
    ) {
        CustomUserDetails userDetails = (CustomUserDetails) authentication.getPrincipal();
        String uid = Objects.requireNonNull(userDetails).getUsername();

        Set<String> roles = authentication.getAuthorities().stream()
                                          .map(GrantedAuthority::getAuthority)
                                          .collect(Collectors.toSet());

        // jwt 발급
        String accessToken = jwtProvider.createAccessToken(uid, roles);
        String[] jtiRefreshToken = jwtProvider.createRefreshToken(uid, roles);

        // refresh jwt 캐싱
        jwtTokenService.cache(uid, jtiRefreshToken[0]);

        // cookie 만들어 내보냄
        var accessCookie = cookieHandler.createCookie("access_token",
                                                      accessToken,
                                                      jwtProvider.getAccessExpirySeconds());
        var refreshCookie = cookieHandler.createCookie("refresh_token",
                                                       jtiRefreshToken[1],
                                                       jwtProvider.getRefreshExpirySeconds());

        response.addHeader(HttpHeaders.SET_COOKIE, accessCookie.toString());
        response.addHeader(HttpHeaders.SET_COOKIE, refreshCookie.toString());
    }
}
