package io.github.seonghun.webapi.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.util.UUID;

@Table(name = "users")
@RequiredArgsConstructor
@Entity
@Getter
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID uid;

    @Column(unique = true, nullable = false, updatable = false)
    private final String userId;

    @Column(unique = false, nullable = false, updatable = true)
    private final String password;

    @Column
    private String username;
}
