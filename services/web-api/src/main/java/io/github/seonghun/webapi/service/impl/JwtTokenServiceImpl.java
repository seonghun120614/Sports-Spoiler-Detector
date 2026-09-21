package io.github.seonghun.webapi.service.impl;

import io.github.seonghun.webapi.common.util.RedisUtil;
import io.github.seonghun.webapi.config.properties.JwtProperty;
import io.github.seonghun.webapi.service.JwtTokenService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class JwtTokenServiceImpl implements JwtTokenService {

    private final JwtProperty jwtProperty;
    private final RedisUtil redisUtil;

    private static final String BLACKLIST_PREFIX = "jwt:blacklist:";
    private static final String CACHE_PREFIX = "jwt:cache:";

    @Override
    public boolean isBlacklisted(String jti) {
        String value = redisUtil.get(BLACKLIST_PREFIX, jti);
        return value != null;
    }

    @Override
    public boolean isValidRefresh(String uid, String refreshJti) {
        return redisUtil.isValidAndEquals(CACHE_PREFIX, uid, refreshJti);
    }

    @Override
    public void blacklist(String jti, long remainingMillis) {
        if (remainingMillis > 0) {
            redisUtil.save(BLACKLIST_PREFIX, jti, "logout", remainingMillis);
        }
    }

    @Override
    public void cacheRefresh(String uid, String refreshJti) {
        redisUtil.save(CACHE_PREFIX, uid, refreshJti, jwtProperty.refreshExpireMilliSeconds());
    }
}
