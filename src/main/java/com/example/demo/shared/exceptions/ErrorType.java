package com.example.demo.shared.exceptions;

import lombok.Getter;

@Getter
public enum ErrorType {

    CATEGORY_NOT_FOUND(1, "category not found", "category does not exists"),
    PRODUCT_NOT_FOUND(2, "product not found", "product does not exists");

    private final int code;
    private final String name;
    public final String message;

    ErrorType(int code, String name, String message){
        this.code = code;
        this.name = name;
        this.message = message;
    }
}
