package io.github.seonghun.webapi.service;

public interface JwtTokenService {

    boolean isBlacklisted(String uid);

    boolean isValidRefresh(String uid, String refreshJti);

    void blacklist(String jti, long remainingMillis);

    void cacheRefresh(String uid, String refreshJti);
}
