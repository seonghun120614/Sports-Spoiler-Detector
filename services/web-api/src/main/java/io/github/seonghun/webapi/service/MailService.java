package io.github.seonghun.webapi.service;

public interface MailService {

    void sendVerificationMail(String email);

    boolean verifyMailCode(String email, String code);
}
