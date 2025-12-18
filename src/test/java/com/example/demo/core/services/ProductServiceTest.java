package com.example.demo.core.services;

import com.example.demo.adapters.dto.ProductRequestDTO;
import com.example.demo.adapters.outbound.repository.ProductRepositoryPort;
import com.example.demo.core.model.Category;
import com.example.demo.core.model.Product;
import com.example.demo.core.port.CategoryServicePort;
import com.example.demo.core.port.ProductServicePort;
import com.example.demo.shared.exceptions.ErrorType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class ProductServiceTest {

    @Mock
    private ProductRepositoryPort productRepository;

    @Mock
    private CategoryServicePort categoryService;

    private ProductServicePort service;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        service = new ProductService(productRepository, categoryService);
    }

    @Test
    void shouldReturnAllProductsWhenCategoryIdIsNull() {
        // arrange
        Product product1 = new Product();
        product1.setId(1L);
        product1.setName("Pizza");

        Product product2 = new Product();
        product2.setId(2L);
        product2.setName("Hambúrguer");

        when(productRepository.findAll())
                .thenReturn(List.of(product1, product2));

        // act
        List<Product> result = service.getAll(null);

        // assert
        assertNotNull(result);
        assertEquals(2, result.size());
        verify(productRepository, times(1)).findAll();
        verifyNoInteractions(categoryService);
    }

    @Test
    void shouldReturnProductsByCategoryWhenCategoryIdIsProvided() {
        // arrange
        Category category = new Category();
        category.setId(1L);
        category.setName("Lanches");

        Product product = new Product();
        product.setId(1L);
        product.setCategory(category);

        when(categoryService.getById(1L))
                .thenReturn(category);
        when(productRepository.findByCategory(category))
                .thenReturn(List.of(product));

        // act
        List<Product> result = service.getAll(1L);

        // assert
        assertNotNull(result);
        assertEquals(1, result.size());
        verify(categoryService, times(1)).getById(1L);
        verify(productRepository, times(1)).findByCategory(category);
    }

    @Test
    void shouldReturnProductWhenFoundById() {
        // arrange
        Product product = new Product();
        product.setId(10L);

        when(productRepository.findById(10L))
                .thenReturn(Optional.of(product));

        // act
        Product result = service.getById(10L);

        // assert
        assertNotNull(result);
        assertEquals(10L, result.getId());
        verify(productRepository, times(1)).findById(10L);
    }

    @Test
    void shouldReturnNullWhenProductNotFoundById() {
        // arrange
        when(productRepository.findById(99L))
                .thenReturn(Optional.empty());

        // act
        Product result = service.getById(99L);

        // assert
        assertNull(result);
        verify(productRepository, times(1)).findById(99L);
    }

    @Test
    void shouldCreateProductSuccessfully() {
        // arrange
        Category category = new Category();
        category.setId(1L);

        ProductRequestDTO dto = new ProductRequestDTO(
                " Pizza ",
                "Pizza italiana",
                new BigDecimal("39.90"),
                "https://cdn.app/pizza.png",
                20,
                1L
        );

        when(categoryService.getById(1L))
                .thenReturn(category);
        when(productRepository.save(any(Product.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        // act
        Product result = service.create(dto);

        // assert
        assertNotNull(result);
        assertEquals("Pizza", result.getName()); // trim validado
        assertEquals(category, result.getCategory());

        verify(categoryService, times(1)).getById(1L);
        verify(productRepository, times(1)).save(any(Product.class));
    }

    @Test
    void shouldUpdateProductSuccessfully() {
        // arrange
        Category category = new Category();
        category.setId(2L);

        Product existingProduct = new Product();
        existingProduct.setId(10L);
        existingProduct.setName("Pizza velha");

        ProductRequestDTO dto = new ProductRequestDTO(
                " Pizza nova ",
                "Pizza atualizada",
                new BigDecimal("42.90"),
                "https://cdn.app/pizza-nova.png",
                25,
                2L
        );

        when(categoryService.getById(2L))
                .thenReturn(category);
        when(productRepository.findById(10L))
                .thenReturn(Optional.of(existingProduct));
        when(productRepository.save(any(Product.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        // act
        Product result = service.update(10L, dto);

        // assert
        assertNotNull(result);
        assertEquals("Pizza nova", result.getName()); // trim validado
        assertEquals(category, result.getCategory());

        verify(categoryService, times(1)).getById(2L);
        verify(productRepository, times(1)).findById(10L);
        verify(productRepository, times(1)).save(existingProduct);
    }

    @Test
    void shouldThrowExceptionWhenUpdatingNonExistingProduct() {
        // arrange
        ProductRequestDTO dto = new ProductRequestDTO(
                "Produto",
                "Desc",
                new BigDecimal("10.00"),
                null,
                5,
                1L
        );

        when(categoryService.getById(1L))
                .thenReturn(new Category());
        when(productRepository.findById(99L))
                .thenReturn(Optional.empty());

        // act + assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> service.update(99L, dto)
        );

        assertEquals(
                ErrorType.PRODUCT_NOT_FOUND.getMessage(),
                exception.getMessage()
        );

        verify(productRepository, never()).save(any());
    }

    @Test
    void shouldDeleteProductById() {
        // act
        service.delete(5L);

        // assert
        verify(productRepository, times(1)).deleteById(5L);
    }

}