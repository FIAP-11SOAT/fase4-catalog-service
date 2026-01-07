package com.example.demo.adapters.dto;

import java.time.OffsetDateTime;
import java.util.UUID;

public record CategoryResponseDTO(
        UUID id,
        String name,
        String description,
        OffsetDateTime createdAt,
        OffsetDateTime updatedAt
) {
}
