package com.example.demo.adapters.inbound;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/categories")
public class CategoryController {

    @GetMapping("/{id}")
    public ResponseEntity<String> get(){
        try {
            return ResponseEntity.ok("");
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
