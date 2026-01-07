package com.example.demo.functional;

import com.example.demo.adapters.dto.ProductRequestDTO;
import com.example.demo.adapters.dto.ProductResponseDTO;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc(addFilters = false)
@ActiveProfiles("test")
class ProductFunctionalTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @WithMockUser(roles = "CUSTOMERS")
    void shouldListAllProducts() throws Exception {

        // act
        MvcResult result = mockMvc.perform(get("/products"))
                .andExpect(status().isOk())
                .andReturn();

        // arrange
        String jsonResponse = result.getResponse().getContentAsString();

        List<ProductResponseDTO> response =
                objectMapper.readValue(
                        jsonResponse,
                        new TypeReference<List<ProductResponseDTO>>() {}
                );

        // assert
        assertEquals(8, response.size());
    }

    @Test
    @WithMockUser(roles = "CUSTOMERS")
    void shouldListAllProductsByCategory() throws Exception {

        // act
        MvcResult result = mockMvc.perform(get("/products?category=44444444-4444-4444-4444-444444444444"))
                .andExpect(status().isOk())
                .andReturn();

        // arrange
        String jsonResponse = result.getResponse().getContentAsString();

        List<ProductResponseDTO> response =
                objectMapper.readValue(
                        jsonResponse,
                        new TypeReference<List<ProductResponseDTO>>() {}
                );

        // assert
        assertEquals(2, response.size());
        assertEquals("Sobremesa", response.getFirst().category());
    }

    @Test
    @WithMockUser(roles = "EMPLOYEES")
    void shouldCreateProduct() throws Exception {
        ProductRequestDTO request = new ProductRequestDTO(
                "Sanduíche de pastrami",
                "Pão italiano com pastrami e molho de ervas",
                BigDecimal.valueOf(29.99),
                "",
                10,
                UUID.fromString("11111111-1111-1111-1111-111111111111")
        );
        String jsonBody = objectMapper.writeValueAsString(request);

        MvcResult result = mockMvc.perform(post("/products")
                .with(csrf())
                .contentType("application/json")
                .content(jsonBody)
        ).andExpect(status().isCreated()).andReturn();

        String jsonResponse = result.getResponse().getContentAsString();

        ProductResponseDTO response =
                objectMapper.readValue(
                        jsonResponse,
                        new TypeReference<ProductResponseDTO>() {}
                );

        assertEquals("Lanche", response.category());
    }
}
