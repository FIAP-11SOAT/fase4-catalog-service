package com.example.demo.core.services;

import com.example.demo.adapters.outbound.repository.CategoryRepositoryPort;
import com.example.demo.adapters.outbound.repository.ProductRepositoryPort;
import com.example.demo.core.model.Category;
import com.example.demo.core.port.CategoryServicePort;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CategoryService implements CategoryServicePort {

    private final CategoryRepositoryPort categoryRepository;

    public CategoryService(CategoryRepositoryPort categoryRepository) {
        this.categoryRepository = categoryRepository;
    }

    @Override
    public List<Category> getAll() {
        return categoryRepository.findAll();
    }

    @Override
    public Category getById(Long id) {
        Optional<Category> category = categoryRepository.findById(id);
        if (category.isEmpty()){
            throw new RuntimeException("Categoria não existe");
        }

        return category.get();
    }
}
