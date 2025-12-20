package com.example.demo.shared.config;

import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.core.convert.converter.Converter;
import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;

public class GrantedAuthoritiesExtractor implements Converter<Jwt, AbstractAuthenticationToken> {

    @Override
    public AbstractAuthenticationToken convert(Jwt jwt) {
        String scopeClaim = jwt.getClaimAsString("user_type");

        Collection<String> scopes = (scopeClaim != null && !scopeClaim.isBlank())
                ? List.of(scopeClaim.trim().split("\\s+"))
                : Collections.emptyList();

        Collection<GrantedAuthority> authorities = scopes.stream()
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .map(s -> "ROLE_" + s.toUpperCase())
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList());

        return new JwtAuthenticationToken(jwt, authorities);
    }
}