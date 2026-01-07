package com.example.demo.adapters.converter;

import com.example.demo.adapters.dto.ProductResponseDTO;
import com.example.demo.core.model.Category;
import com.example.demo.core.model.Product;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ProductConverterTest {

    @Test
    void shouldConvertProductListToProductResponseDTOList() {
        // arrange
        OffsetDateTime createdAt = OffsetDateTime.of(
                2024, 12, 10, 10, 30, 0, 0, ZoneOffset.UTC
        );
        OffsetDateTime updatedAt = OffsetDateTime.of(
                2024, 12, 11, 15, 45, 0, 0, ZoneOffset.UTC
        );

        Category category = new Category();
        category.setId(UUID.fromString("11111111-1111-1111-1111-111111111111"));
        category.setName("Lanches");
        category.setDescription("Categoria de lanches");

        Product product = new Product();
        product.setId(UUID.fromString("11111111-1111-1111-1111-111111111111"));
        product.setName("Hambúrguer");
        product.setDescription("Hambúrguer artesanal");
        product.setPrice(new BigDecimal("29.90"));
        product.setImageUrl("https://cdn.app/hamburguer.png");
        product.setPreparationTime(15);
        product.setCategory(category);
        product.setCreatedAt(createdAt);
        product.setUpdatedAt(updatedAt);

        List<Product> products = List.of(product);

        // act
        List<ProductResponseDTO> result =
                ProductConverter.toResponseDTO(products);

        // assert
        assertNotNull(result);
        assertEquals(1, result.size());

        ProductResponseDTO dto = result.getFirst();

        assertEquals(UUID.fromString("11111111-1111-1111-1111-111111111111"), dto.id());
        assertEquals("Hambúrguer", dto.name());
        assertEquals("Hambúrguer artesanal", dto.description());
        assertEquals(new BigDecimal("29.90"), dto.price());
        assertEquals("https://cdn.app/hamburguer.png", dto.imageUrl());
        assertEquals(15, dto.preparationTime());
        assertEquals("Lanches", dto.category());
        assertEquals(createdAt, dto.createdAt());
        assertEquals(updatedAt, dto.updatedAt());
    }

    @Test
    void shouldReturnEmptyListWhenInputListIsEmpty() {
        // act
        List<ProductResponseDTO> result =
                ProductConverter.toResponseDTO(List.of());

        // assert
        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

}