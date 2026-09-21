package io.github.seonghun.webapi.service.impl;

import io.github.seonghun.webapi.common.util.RedisUtil;
import io.github.seonghun.webapi.domain.Provider;
import io.github.seonghun.webapi.domain.SocialAccount;
import io.github.seonghun.webapi.domain.User;
import io.github.seonghun.webapi.repository.SocialAccountRepository;
import io.github.seonghun.webapi.repository.UserRepository;
import io.github.seonghun.webapi.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final SocialAccountRepository socialAccountRepository;
    private final PasswordEncoder passwordEncoder;
    private final RedisUtil redisUtil;

    @Override
    @Transactional(readOnly = true)
    public boolean exists(String email) {
        return userRepository.findByUserId(email).isPresent();
    }

    @Override
    @Transactional
    public String signUp(String email, String password) {
        var checked = redisUtil.isValidAndEquals("mail-verification", email, "complete");
        if (!checked)
            throw new IllegalArgumentException("Please check your code");
        var user = userRepository.save(new User(email, passwordEncoder.encode(password)));
        return user.getUid().toString();
    }

    @Override
    @Transactional
    public String findOrCreateSocialUser(Provider provider, String providerId, String email) {
        var linked = socialAccountRepository.findByProviderAndProviderId(provider, providerId);
        if (linked.isPresent())
            return linked.get().getUser().getUid().toString();

        var user = userRepository.findByUserId(email)
                                 .orElseGet(() -> userRepository.save(new User(email)));
        socialAccountRepository.save(new SocialAccount(user, provider, providerId));
        return user.getUid().toString();
    }

    @Override
    @Transactional
    public void withdraw(String email, String code) {

    }
}
