package com.example.demo.adapters.inbound;

import com.example.demo.adapters.converter.CategoryConverter;
import com.example.demo.adapters.dto.CategoryResponseDTO;
import com.example.demo.core.model.Category;
import com.example.demo.core.port.CategoryServicePort;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/categories")
@SecurityRequirement(name = "bearerAuth")
public class CategoryController {

    private final CategoryServicePort categoryService;

    public CategoryController(CategoryServicePort categoryService) {
        this.categoryService = categoryService;
    }

    //@PreAuthorize("hasAnyRole('CUSTOMERS', 'EMPLOYEES')")
    @GetMapping("")
    public ResponseEntity<List<CategoryResponseDTO>> get(){
        List<Category> categories = categoryService.getAll();
        List<CategoryResponseDTO> categoryResponseDTOS = CategoryConverter.toResponseDTO(categories);
        return ResponseEntity.ok(categoryResponseDTOS);
    }
}
