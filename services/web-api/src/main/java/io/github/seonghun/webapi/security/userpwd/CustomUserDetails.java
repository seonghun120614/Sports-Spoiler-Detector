package io.github.seonghun.webapi.security.userpwd;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;

@Setter
@Getter
@RequiredArgsConstructor
public class CustomUserDetails implements UserDetails {
    final String username;
    final String password;
    final Collection<? extends GrantedAuthority> authorities;
    boolean accountNonExpired = true;
    boolean accountNonLocked = true;
    boolean credentialsNonExpired = true;
    boolean enabled = true;
}
