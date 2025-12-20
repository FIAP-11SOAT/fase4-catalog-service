package com.example.demo.shared.config;

import java.security.interfaces.RSAPublicKey;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.NimbusJwtDecoder;

import com.nimbusds.jose.jwk.JWK;
import com.nimbusds.jose.jwk.RSAKey;

@Configuration
public class JwtConfig {

    @Value("${JWT_JWK}")
    private String jwkJson;

    @Bean
    public JwtDecoder jwtDecoder() {
        try {
            JWK jwk = JWK.parse(jwkJson);
            RSAKey rsaKey = jwk.toRSAKey();
            RSAPublicKey publicKey = rsaKey.toRSAPublicKey();
            return NimbusJwtDecoder.withPublicKey(publicKey).build();

        } catch (Exception e) {
            throw new RuntimeException("Falha ao carregar ou parsear a chave pública JWK", e);
        }
    }
}
