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
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.http.MediaType;

import org.springframework.security.test.context.support.WithMockUser;


import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ProductController.class)
@ActiveProfiles("test")
class ProductControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ProductServicePort productService;

    @Autowired
    private ObjectMapper objectMapper;

    private Product buildProduct(UUID id) {
        Category category = new Category();
        category.setId(UUID.fromString("11111111-1111-1111-1111-111111111111"));
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
                UUID.fromString("11111111-1111-1111-1111-111111111111")
        );
    }

    @Test
    @WithMockUser(roles = "CUSTOMERS")
    void shouldReturnAllProductsWithoutCategoryFilter() throws Exception {
        when(productService.getAll(null))
                .thenReturn(List.of(buildProduct(UUID.fromString("11111111-1111-1111-1111-111111111111"))));

        mockMvc.perform(get("/products"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].name").value("Hambúrguer"));

        verify(productService).getAll(null);
    }

    @Test
    @WithMockUser(roles = "CUSTOMERS")
    void shouldReturnProductsFilteredByCategory() throws Exception {
        when(productService.getAll(UUID.fromString("11111111-1111-1111-1111-111111111111")))
                .thenReturn(List.of(buildProduct(UUID.fromString("11111111-1111-1111-1111-111111111111"))));

        mockMvc.perform(get("/products")
                        .param("category", "11111111-1111-1111-1111-111111111111"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].category").value("Lanches"));

        verify(productService).getAll(UUID.fromString("11111111-1111-1111-1111-111111111111"));
    }

    @Test
    @WithMockUser(roles = "CUSTOMERS")
    void shouldReturnProductWhenFoundById() throws Exception {
        when(productService.getById(UUID.fromString("11111111-1111-1111-1111-111111111111")))
                .thenReturn(buildProduct(UUID.fromString("11111111-1111-1111-1111-111111111111")));

        mockMvc.perform(get("/products/{id}", UUID.fromString("11111111-1111-1111-1111-111111111111")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value("11111111-1111-1111-1111-111111111111"))
                .andExpect(jsonPath("$.name").value("Hambúrguer"));

        verify(productService).getById(UUID.fromString("11111111-1111-1111-1111-111111111111"));
    }

    @Test
    @WithMockUser(roles = "CUSTOMERS")
    void shouldReturnNoContentWhenProductNotFoundById() throws Exception {
        when(productService.getById(UUID.fromString("91111111-1111-1111-1111-111111111111")))
                .thenReturn(null);

        mockMvc.perform(get("/products/{id}", UUID.fromString("91111111-1111-1111-1111-111111111111")))
                .andExpect(status().isNoContent());

        verify(productService).getById(UUID.fromString("91111111-1111-1111-1111-111111111111"));
    }

    @Test
    @WithMockUser(roles = "EMPLOYEES")
    void shouldCreateProduct() throws Exception {
        Product product = buildProduct(UUID.fromString("11111111-1111-1111-1111-111111111111"));

        when(productService.create(any(ProductRequestDTO.class)))
                .thenReturn(product);

        mockMvc.perform(post("/products")
                        .with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(buildRequestDTO())))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value("11111111-1111-1111-1111-111111111111"))
                .andExpect(jsonPath("$.name").value("Hambúrguer"));

        verify(productService).create(any(ProductRequestDTO.class));
    }

    @Test
    @WithMockUser(roles = "EMPLOYEES")
    void shouldUpdateProduct() throws Exception {
        Product updatedProduct = buildProduct(UUID.fromString("91111111-1111-1111-1111-111111111111"));

        when(productService.update(eq(UUID.fromString("91111111-1111-1111-1111-111111111111")), any(ProductRequestDTO.class)))
                .thenReturn(updatedProduct);

        mockMvc.perform(put("/products/{id}", UUID.fromString("91111111-1111-1111-1111-111111111111"))
                        .with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(buildRequestDTO())))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value("91111111-1111-1111-1111-111111111111"))
                .andExpect(jsonPath("$.name").value("Hambúrguer"));

        verify(productService).update(eq(UUID.fromString("91111111-1111-1111-1111-111111111111")), any(ProductRequestDTO.class));
    }

    @Test
    @WithMockUser(roles = "EMPLOYEES")
    void shouldDeleteProduct() throws Exception {
        mockMvc.perform(delete("/products/{id}", UUID.fromString("51111111-1111-1111-1111-111111111111"))
                .with(csrf()))
                .andExpect(status().isNoContent());

        verify(productService).delete(UUID.fromString("51111111-1111-1111-1111-111111111111"));
    }
}