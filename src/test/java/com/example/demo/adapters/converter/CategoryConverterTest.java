package com.example.demo.adapters.converter;

import com.example.demo.adapters.dto.CategoryResponseDTO;
import com.example.demo.core.model.Category;
import org.junit.jupiter.api.Test;

import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class CategoryConverterTest {

    @Test
    void shouldConvertCategoryListToCategoryResponseDTOList() {
        // arrange
        OffsetDateTime createdAt = OffsetDateTime.of(
                2024, 12, 10, 10, 30, 0, 0, ZoneOffset.UTC
        );
        OffsetDateTime updatedAt = OffsetDateTime.of(
                2024, 12, 11, 15, 45, 0, 0, ZoneOffset.UTC
        );

        Category category = new Category();
        category.setId(1L);
        category.setName("Sobremesa");
        category.setDescription("Doces e sobremesas");
        category.setCreatedAt(createdAt);
        category.setUpdatedAt(updatedAt);

        List<Category> categories = List.of(category);

        // act
        List<CategoryResponseDTO> result =
                CategoryConverter.toResponseDTO(categories);

        // assert
        assertNotNull(result);
        assertEquals(1, result.size());

        CategoryResponseDTO dto = result.getFirst();
        assertEquals(1L, dto.id());
        assertEquals("Sobremesa", dto.name());
        assertEquals("Doces e sobremesas", dto.description());
        assertEquals(createdAt, dto.createdAt());
        assertEquals(updatedAt, dto.updatedAt());
    }

    @Test
    void shouldReturnEmptyListWhenInputListIsEmpty() {
        // act
        List<CategoryResponseDTO> result =
                CategoryConverter.toResponseDTO(List.of());

        // assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

}