package com.example.demo.adapters.outbound.repository;

import com.example.demo.core.model.Category;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface CategoryRepositoryPort extends JpaRepository<Category, UUID> {
}
