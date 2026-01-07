package com.example.demo.core.port;

import com.example.demo.core.model.Category;

import java.util.List;
import java.util.UUID;

public interface CategoryServicePort {
    List<Category> getAll();
    Category getById(UUID id);
}
