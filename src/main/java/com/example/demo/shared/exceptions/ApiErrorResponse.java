package com.example.demo.shared.exceptions;

import lombok.Builder;
import lombok.Getter;

import java.time.OffsetDateTime;

@Getter
@Builder
public class ApiErrorResponse {

    private int status;
    private String error;
    private String message;
    private int errorCode;
    private OffsetDateTime timestamp;

    public ApiErrorResponse(int status, String error, String message, int errorCode, OffsetDateTime timestamp) {
        this.status = status;
        this.error = error;
        this.message = message;
        this.errorCode = errorCode;
        this.timestamp = timestamp;
    }
}
