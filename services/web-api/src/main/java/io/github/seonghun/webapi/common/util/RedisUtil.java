package io.github.seonghun.webapi.common.util;

import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.Duration;

@RequiredArgsConstructor
@Component
public class RedisUtil {
    private final StringRedisTemplate stringRedisTemplate;

    @Transactional
    public void save(String prefix,
                     String userId,
                     String value,
                     long ttlMillis
    ) {
        stringRedisTemplate.opsForValue().set(
                prefix + userId,
                value,
                Duration.ofMillis(ttlMillis)
        );
    }

    @Transactional(readOnly = true)
    public boolean isValidAndEquals(String prefix,
                                    String userId,
                                    String value) {
        String cur = stringRedisTemplate.opsForValue().get(prefix + userId);
        if (cur != null)
            return cur.equals(value);
        return false;
    }

    @Transactional(readOnly = true)
    public String get(String prefix, String userId) {
        return stringRedisTemplate.opsForValue().get(prefix + userId);
    }

    @Transactional
    public void delete(String prefix,
                       String userId) {
        stringRedisTemplate.delete(prefix + userId);
    }
}
