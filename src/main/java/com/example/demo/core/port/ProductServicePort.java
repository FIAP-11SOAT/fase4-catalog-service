package com.example.demo.core.port;

import com.example.demo.adapters.dto.ProductRequestDTO;
import com.example.demo.core.model.Product;

import java.util.List;
import java.util.UUID;

public interface ProductServicePort {
    List<Product> getAll(UUID categoryId);
    Product getById(UUID id);
    Product create(ProductRequestDTO productRequestDTO);
    Product update(UUID id, ProductRequestDTO productRequestDTO);
    void delete(UUID id);
}
