package io.github.seonghun.webapi.security.oauth;

import io.github.seonghun.webapi.common.util.CookieHandler;
import io.github.seonghun.webapi.common.util.JwtProvider;
import io.github.seonghun.webapi.service.JwtTokenService;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Set;

@Component
@RequiredArgsConstructor
public class OAuth2SuccessHandler implements AuthenticationSuccessHandler {

    private static final Set<String> DEFAULT_ROLES = Set.of("ROLE_USER");
    private static final String REDIRECT_URL = "https://bdlddgomjfdlkmoaammpncmaaheibkof.chromiumapp.org/callback";
    private final JwtProvider jwtProvider;
    private final JwtTokenService jwtTokenService;
    private final CookieHandler cookieHandler;

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
                                        HttpServletResponse response,
                                        Authentication authentication
    ) throws IOException, ServletException {
        OidcUser oidcUser = (OidcUser) authentication.getPrincipal();
        String uid = oidcUser.getName();
        String email = oidcUser.getEmail();
        String displayName = oidcUser.getFullName();

        String accessToken = jwtProvider.createAccessToken(uid, DEFAULT_ROLES);
        String[] jtiRefreshToken = jwtProvider.createRefreshToken(uid, DEFAULT_ROLES);

        jwtTokenService.cacheRefresh(uid, jtiRefreshToken[0]);

        var accessCookie = cookieHandler.createCookie("access_token",
                                                      accessToken,
                                                      jwtProvider.getAccessExpirySeconds());
        var refreshCookie = cookieHandler.createCookie("refresh_token",
                                                       jtiRefreshToken[1],
                                                       jwtProvider.getRefreshExpirySeconds());

        response.addHeader(HttpHeaders.SET_COOKIE, accessCookie.toString());
        response.addHeader(HttpHeaders.SET_COOKIE, refreshCookie.toString());

        String fragment = "accessToken=" + encode(accessToken)
                + "&refreshToken=" + encode(jtiRefreshToken[1])
                + "&email=" + encode(email)
                + "&name=" + encode(displayName);

        response.sendRedirect(REDIRECT_URL + "#" + fragment);
    }

    private static String encode(String value) {
        return URLEncoder.encode(value == null ? "" : value, StandardCharsets.UTF_8);
    }
}
