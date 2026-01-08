package com.example.demo.shared.config;

import com.example.demo.shared.exceptions.ApiErrorResponse;
import com.example.demo.shared.exceptions.ErrorType;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.web.SecurityFilterChain;

import java.time.OffsetDateTime;

import static org.springframework.security.config.http.SessionCreationPolicy.STATELESS;


@Configuration
@EnableMethodSecurity(prePostEnabled = true)
public class SecurityConfig {

    private final JwtDecoder jwtDecoder;

    public SecurityConfig(JwtDecoder jwtDecoder) {
        this.jwtDecoder = jwtDecoder;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers(HttpMethod.POST, "/products/**")
                        .hasRole("EMPLOYEES")
                        .requestMatchers(HttpMethod.PUT, "/products/**")
                        .hasRole("EMPLOYEES")
                        .requestMatchers(HttpMethod.DELETE, "/products/**")
                        .hasRole("EMPLOYEES")
                        .requestMatchers(
                                "/swagger-ui.html",
                                "/swagger-ui/**",
                                "/v3/api-docs/**",
                                "/health"
                        ).permitAll()
                        .requestMatchers(HttpMethod.GET, "/products/**").permitAll()
                        .requestMatchers(HttpMethod.GET, "/categories/**").permitAll()
                        .anyRequest().authenticated()
                )
                .oauth2ResourceServer(oauth2 -> oauth2
                        .jwt(jwt -> jwt
                                .decoder(jwtDecoder)
                                .jwtAuthenticationConverter(new GrantedAuthoritiesExtractor())
                        )
                        .authenticationEntryPoint((request, response, authException) -> {
                            response.setContentType(MediaType.APPLICATION_JSON_VALUE);
                            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                            ApiErrorResponse errorResponse = new ApiErrorResponse(
                                    HttpServletResponse.SC_UNAUTHORIZED,
                                    ErrorType.UNAUTHORIZED.getMessage(),
                                    "Unauthorized: " + authException.getMessage(),
                                    ErrorType.UNAUTHORIZED.getCode(),
                                    OffsetDateTime.now()
                            );
                            new ObjectMapper().writeValue(response.getOutputStream(), errorResponse);
                        })
                )
                .csrf(csrf -> csrf.disable())
                .sessionManagement(session -> session.sessionCreationPolicy(STATELESS));

        return http.build();
    }
}
