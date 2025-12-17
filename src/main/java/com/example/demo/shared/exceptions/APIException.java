package com.example.demo.shared.exceptions;

import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
public class APIException extends RuntimeException{

    private final int errorCode;
    private final String errorCodeMessage;
    private final String errorCodeName;
    private final int httpStatus;

    protected APIException(ErrorType errorType, int httpStatus, Exception cause){
        super(errorType.getMessage(), cause);
        this.errorCode = errorType.getCode();
        this.errorCodeName = errorType.getName();
        this.errorCodeMessage = errorType.getMessage();
        this.httpStatus = httpStatus != 0 ? httpStatus : HttpStatus.INTERNAL_SERVER_ERROR.value();
    }
}