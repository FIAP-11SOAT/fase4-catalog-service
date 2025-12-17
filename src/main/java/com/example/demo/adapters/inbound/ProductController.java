package com.example.demo.adapters.inbound;

import com.example.demo.adapters.converter.ProductConverter;
import com.example.demo.adapters.dto.ProductRequestDTO;
import com.example.demo.adapters.dto.ProductResponseDTO;
import com.example.demo.core.model.Product;
import com.example.demo.core.port.ProductServicePort;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/products")
public class ProductController {

    private final ProductServicePort productService;

    public ProductController(ProductServicePort productService) {
        this.productService = productService;
    }

    @GetMapping("")
    public ResponseEntity<?> getAll(@RequestParam(required = false) Long category){
        try {
            List<Product> products = productService.getAll(category);
            List<ProductResponseDTO> productsResponse = ProductConverter.toResponseDTO(products);
            return ResponseEntity.ok(productsResponse);
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getById(@PathVariable Long id){
        try {
            return ResponseEntity.ok("");
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

    @PostMapping("")
    public ResponseEntity<?> create(@RequestBody @Valid ProductRequestDTO productRequestDTO){
        try {
            Product product = productService.create(productRequestDTO);
            List<ProductResponseDTO> productsResponse = ProductConverter.toResponseDTO(List.of(product));
            return ResponseEntity.ok(productsResponse.getFirst());
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> update(@PathVariable Long id, @RequestBody @Valid ProductRequestDTO productRequestDTO){
        try {
            Product productUpdated = productService.update(id, productRequestDTO);
            List<ProductResponseDTO> productsResponse = ProductConverter.toResponseDTO(List.of(productUpdated));
            return ResponseEntity.ok(productsResponse.getFirst());
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> delete(@PathVariable Long id){
        try {
            productService.delete(id);
            return ResponseEntity.ok("");
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

}
