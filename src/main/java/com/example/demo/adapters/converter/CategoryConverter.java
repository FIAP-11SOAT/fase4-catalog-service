package com.example.demo.adapters.converter;

import com.example.demo.adapters.dto.CategoryResponseDTO;
import com.example.demo.core.model.Category;

import java.util.List;

public class CategoryConverter {

    private CategoryConverter() {
    }

    public static List<CategoryResponseDTO> toResponseDTO(List<Category> categories){
        return categories.stream()
                .map(category -> new CategoryResponseDTO(
                        category.getId(),
                        category.getName(),
                        category.getDescription(),
                        category.getCreatedAt(),
                        category.getUpdatedAt()
                ))
                .toList();
    }
}
