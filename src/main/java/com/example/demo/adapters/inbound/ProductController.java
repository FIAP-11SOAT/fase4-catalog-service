package com.example.demo.adapters.inbound;

import com.example.demo.adapters.outbound.repository.RepositoryPort;
import com.example.demo.core.model.Product;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/products")
public class ProductController {

    @Autowired
    private final RepositoryPort repository;

    public ProductController(RepositoryPort repository) {
        this.repository = repository;
    }

    @GetMapping("")
    public ResponseEntity<?> get(){
        try {
            List<Product> products = repository.findAll();
            return ResponseEntity.ok(products);
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

    @PostMapping("/")
    public ResponseEntity<String> create(){
        try {
            return ResponseEntity.ok("");
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

    @PutMapping("/")
    public ResponseEntity<String> edit(){
        try {
            return ResponseEntity.ok("");
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

    @DeleteMapping("/")
    public ResponseEntity<String> delete(){
        try {
            return ResponseEntity.ok("");
        } catch (Exception e){
            return ResponseEntity.internalServerError().body(e.getMessage());
        }
    }

}
