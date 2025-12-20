package com.example.demo.adapters.inbound;

import com.example.demo.core.model.Category;
import com.example.demo.core.port.CategoryServicePort;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(CategoryController.class)
class CategoryControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private CategoryServicePort categoryService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @WithMockUser(roles = "CUSTOMERS")
    void shouldReturnListOfCategories() throws Exception {
        // arrange
        OffsetDateTime createdAt = OffsetDateTime.of(
                2024, 12, 10, 10, 30, 0, 0, ZoneOffset.UTC
        );
        OffsetDateTime updatedAt = OffsetDateTime.of(
                2024, 12, 11, 15, 45, 0, 0, ZoneOffset.UTC
        );

        Category category = new Category();
        category.setId(1L);
        category.setName("Lanches");
        category.setDescription("Categoria de lanches");
        category.setCreatedAt(createdAt);
        category.setUpdatedAt(updatedAt);

        when(categoryService.getAll())
                .thenReturn(List.of(category));

        // act + assert
        mockMvc.perform(get("/categories")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].id").value(1))
                .andExpect(jsonPath("$[0].name").value("Lanches"))
                .andExpect(jsonPath("$[0].description").value("Categoria de lanches"))
                .andExpect(jsonPath("$[0].createdAt").exists())
                .andExpect(jsonPath("$[0].updatedAt").exists());
    }

    @Test
    @WithMockUser(roles = "CUSTOMERS")
    void shouldReturnEmptyListWhenNoCategoriesExist() throws Exception {
        // arrange
        when(categoryService.getAll())
                .thenReturn(List.of());

        // act + assert
        mockMvc.perform(get("/categories"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(0));
    }

}