package io.github.seonghun.webapi.security.oauth;

import io.github.seonghun.webapi.domain.Provider;
import io.github.seonghun.webapi.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.oauth2.core.OAuth2AuthenticationException;
import org.springframework.security.oauth2.core.OAuth2Error;
import org.springframework.security.oauth2.client.oidc.userinfo.OidcUserRequest;
import org.springframework.security.oauth2.client.oidc.userinfo.OidcUserService;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class CustomOidcUserService extends OidcUserService {

    private final UserService userService;

    @Override
    public OidcUser loadUser(OidcUserRequest userRequest) throws OAuth2AuthenticationException {
        OidcUser oidcUser = super.loadUser(userRequest);

        if (!Boolean.TRUE.equals(oidcUser.getEmailVerified()))
            throw new OAuth2AuthenticationException(new OAuth2Error("email_not_verified"),
                                                    "The email of this account is not verified");

        String uid = userService.findOrCreateSocialUser(Provider.GOOGLE,
                                                        oidcUser.getSubject(),
                                                        oidcUser.getEmail());
        return new CustomOidcUser(oidcUser.getAuthorities(),
                                  oidcUser.getIdToken(),
                                  oidcUser.getUserInfo(),
                                  uid);
    }
}
