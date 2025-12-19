package com.example.demo.adapters.inbound;

import com.example.demo.adapters.dto.ProductRequestDTO;
import com.example.demo.core.model.Category;
import com.example.demo.core.model.Product;
import com.example.demo.core.port.ProductServicePort;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.http.MediaType;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ProductController.class)
class ProductControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ProductServicePort productService;

    @Autowired
    private ObjectMapper objectMapper;

    private Product buildProduct(Long id) {
        Category category = new Category();
        category.setId(1L);
        category.setName("Lanches");

        Product product = new Product();
        product.setId(id);
        product.setName("Hambúrguer");
        product.setDescription("Hambúrguer artesanal");
        product.setPrice(new BigDecimal("29.90"));
        product.setImageUrl("https://cdn.app/burger.png");
        product.setPreparationTime(15);
        product.setCategory(category);
        product.setCreatedAt(OffsetDateTime.of(
                2024, 12, 10, 10, 0, 0, 0, ZoneOffset.UTC
        ));
        product.setUpdatedAt(OffsetDateTime.of(
                2024, 12, 11, 12, 0, 0, 0, ZoneOffset.UTC
        ));
        return product;
    }

    private ProductRequestDTO buildRequestDTO() {
        return new ProductRequestDTO(
                " Hambúrguer ",
                "Hambúrguer artesanal",
                new BigDecimal("29.90"),
                "https://cdn.app/burger.png",
                15,
                1L
        );
    }

    /* =========================
       GET /products
       ========================= */

    @Test
    void shouldReturnAllProductsWithoutCategoryFilter() throws Exception {
        when(productService.getAll(null))
                .thenReturn(List.of(buildProduct(1L)));

        mockMvc.perform(get("/products"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].name").value("Hambúrguer"));

        verify(productService).getAll(null);
    }

    @Test
    void shouldReturnProductsFilteredByCategory() throws Exception {
        when(productService.getAll(1L))
                .thenReturn(List.of(buildProduct(1L)));

        mockMvc.perform(get("/products")
                        .param("category", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].category").value("Lanches"));

        verify(productService).getAll(1L);
    }

    /* =========================
       GET /products/{id}
       ========================= */

    @Test
    void shouldReturnProductWhenFoundById() throws Exception {
        when(productService.getById(10L))
                .thenReturn(buildProduct(10L));

        mockMvc.perform(get("/products/{id}", 10L))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(10))
                .andExpect(jsonPath("$.name").value("Hambúrguer"));

        verify(productService).getById(10L);
    }

    @Test
    void shouldReturnNoContentWhenProductNotFoundById() throws Exception {
        when(productService.getById(99L))
                .thenReturn(null);

        mockMvc.perform(get("/products/{id}", 99L))
                .andExpect(status().isNoContent());

        verify(productService).getById(99L);
    }

    /* =========================
       POST /products
       ========================= */

    @Test
    void shouldCreateProduct() throws Exception {
        Product product = buildProduct(1L);

        when(productService.create(any(ProductRequestDTO.class)))
                .thenReturn(product);

        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(buildRequestDTO())))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("Hambúrguer"));

        verify(productService).create(any(ProductRequestDTO.class));
    }

    /* =========================
       PUT /products/{id}
       ========================= */

    @Test
    void shouldUpdateProduct() throws Exception {
        Product updatedProduct = buildProduct(1L);

        when(productService.update(eq(1L), any(ProductRequestDTO.class)))
                .thenReturn(updatedProduct);

        mockMvc.perform(put("/products/{id}", 1L)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(buildRequestDTO())))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("Hambúrguer"));

        verify(productService).update(eq(1L), any(ProductRequestDTO.class));
    }

    /* =========================
       DELETE /products/{id}
       ========================= */

    @Test
    void shouldDeleteProduct() throws Exception {
        mockMvc.perform(delete("/products/{id}", 5L))
                .andExpect(status().isNoContent());

        verify(productService).delete(5L);
    }
}