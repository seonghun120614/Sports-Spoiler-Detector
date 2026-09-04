package io.github.seonghun.webapi.security.jwt;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;

import java.util.Collection;

@Getter
@RequiredArgsConstructor
public class JwtAuthentication implements Authentication {
    final Object principal;
    final Collection<? extends GrantedAuthority> authorities;

    Object credentials = null;
    Object details = null;
    @Setter
    boolean authenticated = true;

    @Override
    public String getName() {
        return principal.toString();
    }
}
