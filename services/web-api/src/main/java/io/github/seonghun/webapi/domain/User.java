package io.github.seonghun.webapi.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import java.util.UUID;

@Table(name = "users")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Entity
@Getter
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID uid;

    @Column(unique = true, nullable = false, updatable = false)
    private String userId;

    @Column(unique = false, nullable = true, updatable = true)
    private String password;

    @Column
    private String username;

    public User(String userId, String password) {
        this.userId = userId;
        this.password = password;
    }

    public User(String userId) {
        this.userId = userId;
    }
}
