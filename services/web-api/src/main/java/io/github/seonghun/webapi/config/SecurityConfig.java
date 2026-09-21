package io.github.seonghun.webapi.config;

import io.github.seonghun.webapi.config.properties.CookieProperty;
import io.github.seonghun.webapi.config.properties.JwtProperty;
import io.github.seonghun.webapi.security.jwt.JwtAuthenticationFilter;
import io.github.seonghun.webapi.security.jwt.JwtRefreshFilter;
import io.github.seonghun.webapi.security.oauth.CustomOidcUserService;
import io.github.seonghun.webapi.security.oauth.OAuth2SuccessHandler;
import io.github.seonghun.webapi.security.userpwd.CustomUserDetailsService;
import io.github.seonghun.webapi.security.userpwd.CustomUsernamePasswordFilter;
import io.github.seonghun.webapi.security.userpwd.UsernamePasswordAuthenticationFailureHandler;
import io.github.seonghun.webapi.security.userpwd.UsernamePasswordAuthenticationManager;
import io.github.seonghun.webapi.security.userpwd.UsernamePasswordAuthenticationSuccessHandler;
import io.github.seonghun.webapi.common.util.CookieHandler;
import io.github.seonghun.webapi.common.util.JwtProvider;
import io.github.seonghun.webapi.service.JwtTokenService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import tools.jackson.databind.ObjectMapper;

import java.util.List;

@Configuration
@RequiredArgsConstructor
@EnableConfigurationProperties({
        CookieProperty.class,
        JwtProperty.class
})
public class SecurityConfig {

    @Value("${spring.security.cors.allowed.origins}")
    private String corsAllowedOrigin;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http,
                                                   CustomUsernamePasswordFilter usernamePasswordFilter,
                                                   JwtAuthenticationFilter jwtAuthenticationFilter,
                                                   JwtRefreshFilter jwtRefreshFilter,
                                                   OAuth2SuccessHandler oAuth2SuccessHandler,
                                                   CustomOidcUserService customOidcUserService
    ) throws Exception {
        return http
                .oauth2Login(oauth2 -> oauth2
                        .authorizationEndpoint(a -> a.baseUri("/api/oauth"))
                        .userInfoEndpoint(u -> u.oidcUserService(customOidcUserService))
                        .successHandler(oAuth2SuccessHandler)
                )
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers(HttpMethod.GET, "/actuator/health").permitAll()
                        .requestMatchers("/error").permitAll()
                        .requestMatchers(HttpMethod.POST,
                                         "/api/login",
                                         "/api/refresh",
                                         "/api/logout",
                                         "/api/users/signup",
                                         "/api/verification/send-mail",
                                         "/api/verification/mail").permitAll()
                        .anyRequest().authenticated()
                )
                .cors(cors -> cors.configurationSource(corsConfigurationSource()))
                .csrf(AbstractHttpConfigurer::disable)
                .formLogin(AbstractHttpConfigurer::disable)
                .httpBasic(AbstractHttpConfigurer::disable)
                .addFilterAt(usernamePasswordFilter, UsernamePasswordAuthenticationFilter.class)
                .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class)
                .addFilterBefore(jwtRefreshFilter, JwtAuthenticationFilter.class)
                .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        var config = new CorsConfiguration();
        config.setAllowedOrigins(List.of(corsAllowedOrigin));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("Content-Type", "Authorization"));
        config.setAllowCredentials(true);   // 쿠키(JWT)를 주고받는다면 필요
        config.setMaxAge(3600L);            // preflight 캐시 1시간

        var source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", config);
        return source;
    }

    @Bean
    public CustomUsernamePasswordFilter usernamePasswordFilter(
            CookieHandler cookieHandler,
            JwtProvider jwtProvider,
            ObjectMapper objectMapper,
            DaoAuthenticationProvider daoAuthenticationProvider,
            JwtTokenService jwtTokenService
    ) {
        final var usernamePasswordAuthenticationManager
                = new UsernamePasswordAuthenticationManager(daoAuthenticationProvider);
        var usernamePasswordFilter = new CustomUsernamePasswordFilter(usernamePasswordAuthenticationManager,
                                                                      objectMapper);

        var usernamePasswordAuthenticationSuccessHandler
                = new UsernamePasswordAuthenticationSuccessHandler(jwtTokenService,
                                                                   jwtProvider,
                                                                   cookieHandler);
        var usernamePasswordAuthenticationFailureHandler
                = new UsernamePasswordAuthenticationFailureHandler(objectMapper);

        usernamePasswordFilter.setAuthenticationSuccessHandler(usernamePasswordAuthenticationSuccessHandler);
        usernamePasswordFilter.setAuthenticationFailureHandler(usernamePasswordAuthenticationFailureHandler);
        return usernamePasswordFilter;
    }

    @Bean
    public DaoAuthenticationProvider daoAuthenticationProvider(
            PasswordEncoder passwordEncoder,
            CustomUserDetailsService userDetailsService
    ) {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder);
        return provider;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
