package io.github.seonghun.webapi.security.userpwd;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationServiceException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter;
import org.springframework.security.web.servlet.util.matcher.PathPatternRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;
import tools.jackson.databind.ObjectMapper;

import java.io.IOException;

public class CustomUsernamePasswordFilter extends AbstractAuthenticationProcessingFilter {
    public static final String USER_ID_KEY = "id";
    public static final String PASSWORD_KEY = "password";

    private static final RequestMatcher DEFAULT_PATH_REQUEST_MATCHER = PathPatternRequestMatcher
            .withDefaults().matcher(HttpMethod.POST, "/api/login");

    private final ObjectMapper objectMapper;

    public CustomUsernamePasswordFilter(ObjectMapper objectMapper) {
        super(DEFAULT_PATH_REQUEST_MATCHER);
        this.objectMapper = objectMapper;
    }

    public CustomUsernamePasswordFilter(AuthenticationManager authenticationManager, ObjectMapper objectMapper) {
        super(DEFAULT_PATH_REQUEST_MATCHER, authenticationManager);
        this.objectMapper = objectMapper;
    }

    @Override
    public Authentication attemptAuthentication(HttpServletRequest request,
                                                HttpServletResponse response) {
        // Filtering
        String contentType = request.getContentType();
        if (!request.getMethod().equals("POST"))
            throw new AuthenticationServiceException("Authentication method not supported: " + request.getMethod());
        if (contentType == null)
            throw new AuthenticationServiceException("Authentication method not supported: null");

        // Parsing
        LoginRequest loginRequest = null;
        if (contentType.contains(MediaType.APPLICATION_JSON_VALUE))
            loginRequest = jsonParsing(request);
        else if (contentType.contains(MediaType.APPLICATION_FORM_URLENCODED_VALUE))
            loginRequest = formParsing(request);
        else
            throw new AuthenticationServiceException("Authentication method not supported: " + contentType);

        // Auth
        validate(loginRequest);
        UsernamePasswordAuthentication authRequest
                = new UsernamePasswordAuthentication(loginRequest.userId(), loginRequest.password());
        Authentication auth = this.getAuthenticationManager().authenticate(authRequest);
        return auth;
    }

    private void validate(LoginRequest req) {
        if (req.userId() == null || req.password() == null ||
                req.userId().isBlank() || req.password().isBlank())
            throw new AuthenticationServiceException("잘못된 입력입니다.");
    }

    private LoginRequest formParsing(HttpServletRequest request) {
        String userId = request.getParameter(USER_ID_KEY);
        String password = request.getParameter(PASSWORD_KEY);
        if (userId == null || password == null)
            userId = password = "";
        return new LoginRequest(userId, password);
    }

    private LoginRequest jsonParsing(HttpServletRequest request) throws AuthenticationException {
        try {
            var loginRequest = objectMapper.readValue(request.getInputStream(), LoginRequest.class);
            return loginRequest;
        } catch (IOException e) {
            throw new AuthenticationServiceException("로그인 요청 본문 파싱 실패", e);
        }
    }

    private record LoginRequest(String userId, String password) {}
}
