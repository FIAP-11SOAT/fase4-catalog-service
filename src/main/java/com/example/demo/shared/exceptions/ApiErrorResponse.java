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
}
