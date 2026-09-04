package io.github.seonghun.webapi.config;

import io.github.seonghun.webapi.config.properties.CookieProperty;
import io.github.seonghun.webapi.config.properties.JwtProperty;
import io.github.seonghun.webapi.security.jwt.JwtAuthenticationFilter;
import io.github.seonghun.webapi.security.jwt.JwtRefreshFilter;
import io.github.seonghun.webapi.security.userpwd.CustomUserDetailsService;
import io.github.seonghun.webapi.security.userpwd.CustomUsernamePasswordFilter;
import io.github.seonghun.webapi.security.userpwd.UsernamePasswordAuthenticationFailureHandler;
import io.github.seonghun.webapi.security.userpwd.UsernamePasswordAuthenticationManager;
import io.github.seonghun.webapi.security.userpwd.UsernamePasswordAuthenticationSuccessHandler;
import io.github.seonghun.webapi.common.util.CookieHandler;
import io.github.seonghun.webapi.common.util.JwtProvider;
import io.github.seonghun.webapi.service.JwtTokenService;
import lombok.RequiredArgsConstructor;
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
import tools.jackson.databind.ObjectMapper;

@Configuration
@RequiredArgsConstructor
@EnableConfigurationProperties({
        CookieProperty.class,
        JwtProperty.class
})
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http,
                                                   CustomUsernamePasswordFilter usernamePasswordFilter,
                                                   JwtAuthenticationFilter jwtAuthenticationFilter,
                                                   JwtRefreshFilter jwtRefreshFilter) throws Exception {
        return http
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers(HttpMethod.POST, "/api/login", "/api/refresh", "/api/logout").permitAll()
                        .anyRequest().authenticated()
                )
                .cors(AbstractHttpConfigurer::disable)
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
