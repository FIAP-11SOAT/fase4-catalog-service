package com.example.demo.shared.exceptions;

import org.springframework.http.HttpStatus;

public class ExceptionUtils {

    private ExceptionUtils() {
        // Construtor privado para evitar instanciação
    }

    public static APIException exception(
            ErrorType errorType, int httpStatus, Exception exception
    ) {
        return new APIException(errorType, httpStatus, exception);
    }

    public static APIException badRequest(ErrorType errorType, Exception exception) {
        return exception(errorType, HttpStatus.BAD_REQUEST.value(), exception);
    }

    public static APIException internalError(ErrorType errorType, Exception exception) {
        return exception(errorType, HttpStatus.INTERNAL_SERVER_ERROR.value(), exception);
    }
}