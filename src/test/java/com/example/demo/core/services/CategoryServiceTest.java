package com.example.demo.core.services;

import com.example.demo.adapters.outbound.repository.CategoryRepositoryPort;
import com.example.demo.core.model.Category;
import com.example.demo.core.port.CategoryServicePort;
import com.example.demo.shared.exceptions.ErrorType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class CategoryServiceTest {

    @Mock
    private CategoryRepositoryPort categoryRepository;

    private CategoryServicePort service;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        service = new CategoryService(categoryRepository);
    }

    @Test
    void shouldReturnAllCategories() {
        // arrange
        Category category1 = new Category();
        category1.setId(UUID.fromString("11111111-1111-1111-1111-111111111111"));
        category1.setName("Lanches");

        Category category2 = new Category();
        category2.setId(UUID.fromString("21111111-1111-1111-1111-111111111111"));
        category2.setName("Bebidas");

        when(categoryRepository.findAll())
                .thenReturn(List.of(category1, category2));

        // act
        List<Category> result = service.getAll();

        // assert
        assertNotNull(result);
        assertEquals(2, result.size());
        assertEquals("Lanches", result.get(0).getName());
        assertEquals("Bebidas", result.get(1).getName());

        verify(categoryRepository, times(1)).findAll();
    }

    @Test
    void shouldReturnCategoryWhenFoundById() {
        // arrange
        Category category = new Category();
        category.setId(UUID.fromString("11111111-1111-1111-1111-111111111111"));
        category.setName("Lanches");

        when(categoryRepository.findById(UUID.fromString("11111111-1111-1111-1111-111111111111")))
                .thenReturn(Optional.of(category));

        // act
        Category result = service.getById(UUID.fromString("11111111-1111-1111-1111-111111111111"));

        // assert
        assertNotNull(result);
        assertEquals(UUID.fromString("11111111-1111-1111-1111-111111111111"), result.getId());
        assertEquals("Lanches", result.getName());

        verify(categoryRepository, times(1)).findById(UUID.fromString("11111111-1111-1111-1111-111111111111"));
    }

    @Test
    void shouldThrowExceptionWhenCategoryNotFound() {
        // arrange
        when(categoryRepository.findById(UUID.fromString("91111111-1111-1111-1111-111111111111")))
                .thenReturn(Optional.empty());

        // act + assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> service.getById(UUID.fromString("91111111-1111-1111-1111-111111111111"))
        );

        assertEquals(
                ErrorType.CATEGORY_NOT_FOUND.getMessage(),
                exception.getMessage()
        );

        verify(categoryRepository, times(1)).findById(UUID.fromString("91111111-1111-1111-1111-111111111111"));
    }

}