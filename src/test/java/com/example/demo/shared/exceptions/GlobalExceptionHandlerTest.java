package com.example.demo.shared.exceptions;

import jakarta.validation.Valid;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.core.MethodParameter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authorization.AuthorizationDeniedException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.servlet.NoHandlerFoundException;

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.*;

class GlobalExceptionHandlerTest {

    private GlobalExceptionHandler handler;

    @BeforeEach
    void setUp() {
        handler = new GlobalExceptionHandler();
    }

    @Test
    void shouldHandleApiException() {
        APIException exception = new APIException(
                ErrorType.CATEGORY_NOT_FOUND,
                400,
                null
        );

        ResponseEntity<ApiErrorResponse> response =
                handler.handleCatalogApiException(exception);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());

        ApiErrorResponse body = response.getBody();
        assertNotNull(body);
        assertEquals(400, body.getStatus());
        assertEquals("Bad Request", body.getError());
        assertEquals(ErrorType.CATEGORY_NOT_FOUND.getMessage(), body.getMessage());
        assertEquals(ErrorType.CATEGORY_NOT_FOUND.getCode(), body.getErrorCode());
        assertNotNull(body.getTimestamp());
    }

    @Test
    void shouldHandleMethodArgumentNotValidException() throws Exception {
        BeanPropertyBindingResult bindingResult =
                new BeanPropertyBindingResult(new Object(), "request");

        bindingResult.addError(
                new FieldError("request", "name", "must not be blank")
        );

        Method method = this.getClass()
                .getDeclaredMethod("dummyMethod", Object.class);

        MethodParameter methodParameter =
                new MethodParameter(method, 0);

        MethodArgumentNotValidException exception =
                new MethodArgumentNotValidException(methodParameter, bindingResult);

        ResponseEntity<ApiErrorResponse> response =
                handler.handleMethodArgumentNotValid(exception);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());

        ApiErrorResponse body = response.getBody();
        assertNotNull(body);
        assertEquals(400, body.getStatus());
        assertEquals("Bad Request", body.getError());
        assertEquals("name: must not be blank", body.getMessage());
        assertEquals(400, body.getErrorCode());
        assertNotNull(body.getTimestamp());
    }

    @SuppressWarnings("unused")
    private void dummyMethod(@Valid Object request) {
        // Método intencionalmente vazio.
        // Usado apenas para forçar a validação Bean Validation (@Valid)
        // em contextos onde não há um endpoint ou método público.
    }

    @Test
    void shouldHandleNoHandlerFoundException() {
        NoHandlerFoundException exception =
                new NoHandlerFoundException(
                        "GET",
                        "/rota-inexistente",
                        null
                );

        ResponseEntity<ApiErrorResponse> response =
                handler.handleNoHandlerFound(exception);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());

        ApiErrorResponse body = response.getBody();
        assertNotNull(body);
        assertEquals(404, body.getStatus());
        assertEquals("Not Found", body.getError());
        assertEquals("Route not found", body.getMessage());
        assertEquals(404, body.getErrorCode());
        assertNotNull(body.getTimestamp());
    }

    @Test
    void shouldHandleAuthenticationException() {
        AuthenticationException exception =
                new BadCredentialsException("Invalid token");

        ResponseEntity<ApiErrorResponse> response =
                handler.handleAuthenticationException(exception);

        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());

        ApiErrorResponse body = response.getBody();
        assertNotNull(body);
        assertEquals(401, body.getStatus());
        assertEquals(ErrorType.UNAUTHORIZED.getMessage(), body.getError());
        assertEquals("Invalid token", body.getMessage());
        assertEquals(ErrorType.UNAUTHORIZED.getCode(), body.getErrorCode());
        assertNotNull(body.getTimestamp());
    }

    @Test
    void shouldHandleAccessDeniedException() {
        AccessDeniedException exception =
                new AccessDeniedException("Access is denied");

        ResponseEntity<ApiErrorResponse> response =
                handler.handleAuthenticationException(exception);

        assertEquals(HttpStatus.FORBIDDEN, response.getStatusCode());

        ApiErrorResponse body = response.getBody();
        assertNotNull(body);
        assertEquals(403, body.getStatus());
        assertEquals(ErrorType.FORBIDDEN.getMessage(), body.getError());
        assertEquals("Access is denied", body.getMessage());
        assertEquals(ErrorType.FORBIDDEN.getCode(), body.getErrorCode());
        assertNotNull(body.getTimestamp());
    }

    @Test
    void shouldHandleAuthorizationDeniedException() {
        AuthorizationDeniedException exception =
                new AuthorizationDeniedException(
                "Authorization denied",
                () -> false
        );

        ResponseEntity<ApiErrorResponse> response =
                handler.handleAuthenticationException(exception);

        assertEquals(HttpStatus.FORBIDDEN, response.getStatusCode());

        ApiErrorResponse body = response.getBody();
        assertNotNull(body);
        assertEquals(403, body.getStatus());
        assertEquals(ErrorType.FORBIDDEN.getMessage(), body.getError());
        assertEquals("Authorization denied", body.getMessage());
        assertEquals(ErrorType.FORBIDDEN.getCode(), body.getErrorCode());
        assertNotNull(body.getTimestamp());
    }

    @Test
    void shouldHandleGenericException() {
        Exception exception = new RuntimeException("boom");

        ResponseEntity<ApiErrorResponse> response =
                handler.handleGenericException(exception);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());

        ApiErrorResponse body = response.getBody();
        assertNotNull(body);
        assertEquals(500, body.getStatus());
        assertEquals("Internal Server Error", body.getError());
        assertEquals("Unexpected internal error", body.getMessage());
        assertEquals(999, body.getErrorCode());
        assertNotNull(body.getTimestamp());
    }
}


