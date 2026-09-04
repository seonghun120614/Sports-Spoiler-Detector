package io.github.seonghun.webapi.service.impl;

import io.github.seonghun.webapi.service.JwtTokenService;
import org.springframework.stereotype.Service;

@Service
public class JwtTokenServiceImpl implements JwtTokenService {
    @Override
    public boolean isBlacklisted(String uid) {
        return false;
    }

    @Override
    public void blacklist(String jti, long remainingMillis) {

    }

    @Override
    public void cache(String name, String s) {

    }
}
