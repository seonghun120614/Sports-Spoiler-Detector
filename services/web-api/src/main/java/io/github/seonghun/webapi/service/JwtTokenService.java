package io.github.seonghun.webapi.service;

public interface JwtTokenService {

    boolean isBlacklisted(String uid);

    void blacklist(String jti, long remainingMillis);

    void cache(String name, String s);
}
