package io.github.seonghun.webapi.repository;

import io.github.seonghun.webapi.domain.Provider;
import io.github.seonghun.webapi.domain.SocialAccount;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface SocialAccountRepository extends JpaRepository<SocialAccount, UUID> {
    Optional<SocialAccount> findByProviderAndProviderId(Provider provider, String providerId);
}
