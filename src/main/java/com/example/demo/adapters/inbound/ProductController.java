package com.example.demo.adapters.inbound;

import com.example.demo.adapters.converter.ProductConverter;
import com.example.demo.adapters.dto.ProductRequestDTO;
import com.example.demo.adapters.dto.ProductResponseDTO;
import com.example.demo.core.model.Product;
import com.example.demo.core.port.ProductServicePort;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
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
    public ResponseEntity<List<ProductResponseDTO>> getAll(@RequestParam(required = false) Long category){
        List<Product> products = productService.getAll(category);
        List<ProductResponseDTO> productsResponse = ProductConverter.toResponseDTO(products);
        return ResponseEntity.ok(productsResponse);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProductResponseDTO> getById(@PathVariable Long id){
        Product product = productService.getById(id);
        if(product == null){
            return ResponseEntity.noContent().build();
        }
        List<ProductResponseDTO> productsResponse = ProductConverter.toResponseDTO(List.of(product));
        return ResponseEntity.ok(productsResponse.getFirst());
    }

    @PostMapping("")
    public ResponseEntity<ProductResponseDTO> create(@RequestBody @Valid ProductRequestDTO productRequestDTO){
        Product product = productService.create(productRequestDTO);
        List<ProductResponseDTO> productsResponse = ProductConverter.toResponseDTO(List.of(product));
        return ResponseEntity.status(HttpStatus.CREATED).body(productsResponse.getFirst());
    }

    @PutMapping("/{id}")
    public ResponseEntity<ProductResponseDTO> update(@PathVariable Long id, @RequestBody @Valid ProductRequestDTO productRequestDTO){
        Product productUpdated = productService.update(id, productRequestDTO);
        List<ProductResponseDTO> productsResponse = ProductConverter.toResponseDTO(List.of(productUpdated));
        return ResponseEntity.ok(productsResponse.getFirst());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id){
        productService.delete(id);
        return ResponseEntity.noContent().build();
    }

}
