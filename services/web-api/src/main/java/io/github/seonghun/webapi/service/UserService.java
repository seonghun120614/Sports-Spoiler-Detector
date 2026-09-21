package io.github.seonghun.webapi.service;

import io.github.seonghun.webapi.domain.Provider;

public interface UserService {

    boolean exists(String email);

    String signUp(String email, String password);

    String findOrCreateSocialUser(Provider provider, String providerId, String email);

    void withdraw(String email, String code);
}
