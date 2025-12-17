package com.example.demo.adapters.inbound;

import com.example.demo.adapters.converter.CategoryConverter;
import com.example.demo.adapters.dto.CategoryResponseDTO;
import com.example.demo.core.model.Category;
import com.example.demo.core.port.CategoryServicePort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/categories")
public class CategoryController {

    private final CategoryServicePort categoryService;

    public CategoryController(CategoryServicePort categoryService) {
        this.categoryService = categoryService;
    }

    @GetMapping("")
    public ResponseEntity<?> get(){
        try {
            List<Category> categories = categoryService.getAll();
            List<CategoryResponseDTO> categoryResponseDTOS = CategoryConverter.toResponseDTO(categories);
            return ResponseEntity.ok(categoryResponseDTOS);
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }
}
