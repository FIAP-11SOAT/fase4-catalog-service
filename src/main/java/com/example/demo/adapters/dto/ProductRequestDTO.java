package com.example.demo.adapters.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.*;

import java.math.BigDecimal;
import java.util.UUID;

public record ProductRequestDTO(

        @NotBlank
        @Size(max = 150)
        String name,

        @Size(max = 1000)
        String description,

        @NotNull
        @DecimalMin(value = "0.00", inclusive = true)
        @Digits(integer = 10, fraction = 2)
        BigDecimal price,

        @Size(max = 500)
        String imageUrl,

        @NotNull
        @Min(0)
        @JsonProperty("preparation_time")
        Integer preparationTime,

        @NotNull
        @JsonProperty("category_id")
        UUID categoryId
) {
}
