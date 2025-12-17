package com.example.demo.adapters.outbound.repository;

import com.example.demo.core.model.Category;
import com.example.demo.core.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ProductRepositoryPort extends JpaRepository<Product, Long> {
    List<Product> findByCategory(Category category);
}
