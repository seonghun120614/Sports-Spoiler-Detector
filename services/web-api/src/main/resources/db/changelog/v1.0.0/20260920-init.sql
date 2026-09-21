--liquibase formatted sql

--changeset seonghun:20260920-01-create-users
--preconditions onFail:MARK_RAN
--precondition-sql-check expectedResult:0 SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'users'
CREATE TABLE users (
    uid      UUID         PRIMARY KEY,
    user_id  VARCHAR(255) NOT NULL,
    password VARCHAR(255),
    username VARCHAR(255),
    CONSTRAINT uk_users_user_id UNIQUE (user_id)
);
--rollback DROP TABLE users;

--changeset seonghun:20260920-02-create-social-accounts
--preconditions onFail:MARK_RAN
--precondition-sql-check expectedResult:0 SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'social_accounts'
CREATE TABLE social_accounts (
    uid         UUID         PRIMARY KEY,
    user_uid    UUID         NOT NULL,
    provider    VARCHAR(255) NOT NULL,
    provider_id VARCHAR(255) NOT NULL,
    CONSTRAINT fk_social_accounts_user FOREIGN KEY (user_uid) REFERENCES users (uid),
    CONSTRAINT uk_social_accounts_provider UNIQUE (provider, provider_id)
);
--rollback DROP TABLE social_accounts;
