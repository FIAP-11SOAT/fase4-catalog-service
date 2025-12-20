package com.example.demo.stepdefs;

import com.example.demo.adapters.dto.ProductResponseDTO;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ActiveProfiles("test")
public class CatalogStepDefs {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    // estado compartilhado entre os passos do cenário
    private String categoryId;
    private MvcResult mvcResult;
    private List<ProductResponseDTO> products;

    @Given("a valid category id")
    public void valid_category_id() {
        this.categoryId = "4";
    }

    @When("a GET request is sent to {string}")
    public void get_request_sent_to(String endpoint) throws Exception {
        mvcResult = mockMvc.perform(
                        get(endpoint + "?category=" + categoryId)
                                .with(user("test-user").roles("CUSTOMERS"))
                )
                .andExpect(status().isOk())
                .andReturn();

        String json = mvcResult.getResponse().getContentAsString();
        products = objectMapper.readValue(
                json,
                new TypeReference<List<ProductResponseDTO>>() {}
        );
    }

    @Then("a list of products for the given category should be returned")
    public void a_list_of_products_should_be_returned() {
        assertEquals(2, products.size());
        assertEquals("Sobremesa", products.getFirst().category());
    }
}
