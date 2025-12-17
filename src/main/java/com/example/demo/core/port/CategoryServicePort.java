package com.example.demo.core.port;

import com.example.demo.core.model.Category;

import java.util.List;

public interface CategoryServicePort {
    List<Category> getAll();
    Category getById(Long id);
}
