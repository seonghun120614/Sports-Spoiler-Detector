package io.github.seonghun.webapi.common.util;

import org.springframework.stereotype.Component;
import java.security.SecureRandom;

@Component
public class RandomGenerator {

    private static final String NUMBERS = "0123456789";
    private static final String UPPER_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private static final String LOWER_LETTERS = "abcdefghijklmnopqrstuvwxyz";
    private static final String ALPHABET = UPPER_LETTERS + LOWER_LETTERS;
    private static final String ALPHANUMERIC = ALPHABET + NUMBERS;
//    private static final String SPECIAL_CHARS = "!@#$%^&*()-_=+";

    private final SecureRandom secureRandom = new SecureRandom();

//    public String generateNumeric(int length) {
//        return buildRandomString(NUMBERS, length);
//    }
//
//    public String generateAlphabetic(int length) {
//        return buildRandomString(ALPHABET, length);
//    }

    public String generateAlphanumeric(int length) {
        return buildRandomString(ALPHANUMERIC, length);
    }

//    public String generateComplexPassword(int length) {
//        return buildRandomString(ALPHANUMERIC + SPECIAL_CHARS, length);
//    }

    private String buildRandomString(String characterPool, int length) {
        if (length <= 0) {
            throw new IllegalArgumentException("길이는 1 이상이어야 합니다.");
        }

        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            int randomIndex = secureRandom.nextInt(characterPool.length());
            sb.append(characterPool.charAt(randomIndex));
        }
        return sb.toString();
    }
}