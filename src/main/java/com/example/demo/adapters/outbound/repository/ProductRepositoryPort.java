package com.example.demo.adapters.outbound.repository;

import com.example.demo.core.model.Category;
import com.example.demo.core.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface ProductRepositoryPort extends JpaRepository<Product, UUID> {
    List<Product> findByCategory(Category category);
}
