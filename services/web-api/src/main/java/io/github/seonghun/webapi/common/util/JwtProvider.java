package io.github.seonghun.webapi.common.util;

import io.github.seonghun.webapi.config.properties.JwtProperty;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.Set;
import java.util.UUID;

@Component
@RequiredArgsConstructor
public class JwtProvider {
    private final JwtProperty jwtProperty;
    private SecretKey key;

    @PostConstruct
    void init() {
        this.key = Keys.hmacShaKeyFor(
                jwtProperty.secret().getBytes()
        );
    }

    public String createAccessToken(String username,
                                    Set<String> roles) {
        Date now = new Date();
        Date expiry = new Date(now.getTime() + jwtProperty.accessExpireMilliSeconds());

        return Jwts.builder()
                   .subject(username)
                   .claim("roles", roles)
                   .issuedAt(now)
                   .expiration(expiry)
                   .signWith(key)
                   .compact();
    }

    public String[] createRefreshToken(String username,
                                       Set<String> roles) {
        String jti = UUID.randomUUID().toString();
        Date now = new Date();
        Date expiry = new Date(now.getTime() + jwtProperty.refreshExpireMilliSeconds());

        return new String[] {
                jti,
                Jwts.builder()
                    .id(jti)
                    .subject(username)
                    .claim("roles", roles)
                    .issuedAt(now)
                    .expiration(expiry)
                    .signWith(key)
                        .compact()
        };
    }

    public Claims parse(String token) {
        return Jwts.parser()
                   .verifyWith(key)
                   .build()
                   .parseSignedClaims(token)
                   .getPayload();
    }

    public long getAccessExpirySeconds() {
        return jwtProperty.accessExpireMilliSeconds();
    }

    public long getRefreshExpirySeconds() {
        return jwtProperty.refreshExpireMilliSeconds();
    }
}
