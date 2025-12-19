package com.example.demo.adapters.dto;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

public record ProductResponseDTO(
        Long id,
        String name,
        String description,
        BigDecimal price,
        String imageUrl,
        Integer preparationTime,
        String category,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt
) {
}
