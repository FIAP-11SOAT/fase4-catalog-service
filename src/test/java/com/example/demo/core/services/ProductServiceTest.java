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
import java.util.UUID;

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
        product1.setId(UUID.fromString("11111111-1111-1111-1111-111111111111"));
        product1.setName("Pizza");

        Product product2 = new Product();
        product2.setId(UUID.fromString("22222222-2222-2222-2222-222222222222"));
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
        category.setId(UUID.fromString("11111111-1111-1111-1111-111111111111"));
        category.setName("Lanches");

        Product product = new Product();
        product.setId(UUID.fromString("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"));
        product.setCategory(category);

        UUID categoryId = UUID.fromString("11111111-1111-1111-1111-111111111111");

        when(categoryService.getById(categoryId))
                .thenReturn(category);
        when(productRepository.findByCategory(category))
                .thenReturn(List.of(product));

        // act
        List<Product> result = service.getAll(categoryId);

        // assert
        assertNotNull(result);
        assertEquals(1, result.size());
        verify(categoryService, times(1)).getById(categoryId);
        verify(productRepository, times(1)).findByCategory(category);
    }

    @Test
    void shouldReturnProductWhenFoundById() {
        // arrange
        UUID productId = UUID.fromString("10101010-1010-1010-1010-101010101010");

        Product product = new Product();
        product.setId(productId);

        when(productRepository.findById(productId))
                .thenReturn(Optional.of(product));

        // act
        Product result = service.getById(productId);

        // assert
        assertNotNull(result);
        assertEquals(productId, result.getId());
        verify(productRepository, times(1)).findById(productId);
    }

    @Test
    void shouldReturnNullWhenProductNotFoundById() {
        // arrange
        UUID productId = UUID.fromString("99999999-9999-9999-9999-999999999999");

        when(productRepository.findById(productId))
                .thenReturn(Optional.empty());

        // act
        Product result = service.getById(productId);

        // assert
        assertNull(result);
        verify(productRepository, times(1)).findById(productId);
    }

    @Test
    void shouldCreateProductSuccessfully() {
        // arrange
        UUID categoryId = UUID.fromString("11111111-1111-1111-1111-111111111111");

        Category category = new Category();
        category.setId(categoryId);

        ProductRequestDTO dto = new ProductRequestDTO(
                " Pizza ",
                "Pizza italiana",
                new BigDecimal("39.90"),
                "https://cdn.app/pizza.png",
                20,
                categoryId
        );

        when(categoryService.getById(categoryId))
                .thenReturn(category);
        when(productRepository.save(any(Product.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        // act
        Product result = service.create(dto);

        // assert
        assertNotNull(result);
        assertEquals("Pizza", result.getName()); // trim validado
        assertEquals(category, result.getCategory());

        verify(categoryService, times(1)).getById(categoryId);
        verify(productRepository, times(1)).save(any(Product.class));
    }

    @Test
    void shouldUpdateProductSuccessfully() {
        // arrange
        UUID categoryId = UUID.fromString("22222222-2222-2222-2222-222222222222");
        UUID productId = UUID.fromString("10101010-1010-1010-1010-101010101010");

        Category category = new Category();
        category.setId(categoryId);

        Product existingProduct = new Product();
        existingProduct.setId(productId);
        existingProduct.setName("Pizza velha");

        ProductRequestDTO dto = new ProductRequestDTO(
                " Pizza nova ",
                "Pizza atualizada",
                new BigDecimal("42.90"),
                "https://cdn.app/pizza-nova.png",
                25,
                categoryId
        );

        when(categoryService.getById(categoryId))
                .thenReturn(category);
        when(productRepository.findById(productId))
                .thenReturn(Optional.of(existingProduct));
        when(productRepository.save(any(Product.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        // act
        Product result = service.update(productId, dto);

        // assert
        assertNotNull(result);
        assertEquals("Pizza nova", result.getName()); // trim validado
        assertEquals(category, result.getCategory());

        verify(categoryService, times(1)).getById(categoryId);
        verify(productRepository, times(1)).findById(productId);
        verify(productRepository, times(1)).save(existingProduct);
    }

    @Test
    void shouldThrowExceptionWhenUpdatingNonExistingProduct() {
        // arrange
        UUID categoryId = UUID.fromString("11111111-1111-1111-1111-111111111111");
        UUID nonExistingProductId = UUID.fromString("99999999-9999-9999-9999-999999999999");

        ProductRequestDTO dto = new ProductRequestDTO(
                "Produto",
                "Desc",
                new BigDecimal("10.00"),
                null,
                5,
                categoryId
        );

        when(categoryService.getById(categoryId))
                .thenReturn(new Category());
        when(productRepository.findById(nonExistingProductId))
                .thenReturn(Optional.empty());

        // act + assert
        RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> service.update(nonExistingProductId, dto)
        );

        assertEquals(
                ErrorType.PRODUCT_NOT_FOUND.getMessage(),
                exception.getMessage()
        );

        verify(productRepository, never()).save(any());
    }

    @Test
    void shouldDeleteProductById() {
        UUID idToDelete = UUID.fromString("51111111-1111-1111-1111-111111111111");

        // act
        service.delete(idToDelete);

        // assert
        verify(productRepository, times(1)).deleteById(idToDelete);
    }

}
