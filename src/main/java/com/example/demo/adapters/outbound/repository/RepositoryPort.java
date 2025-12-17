package com.example.demo.adapters.outbound.repository;

import com.example.demo.core.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RepositoryPort extends JpaRepository<Product, Long> {
}
