package com.example.demo.adapters.dto;

import java.time.OffsetDateTime;

public record CategoryResponseDTO(
        Long id,
        String name,
        String description,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt
) {
}
