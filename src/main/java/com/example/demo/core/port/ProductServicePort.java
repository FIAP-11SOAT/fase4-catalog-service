package com.example.demo.core.port;

import com.example.demo.adapters.dto.ProductRequestDTO;
import com.example.demo.core.model.Product;

import java.util.List;

public interface ProductServicePort {
    List<Product> getAll(Long categoryId);
    Product getById(Long id);
    Product create(ProductRequestDTO productRequestDTO);
    Product update(Long id, ProductRequestDTO productRequestDTO);
    void delete(Long id);
}
