package com.example.demo.adapters.converter;

import com.example.demo.adapters.dto.ProductResponseDTO;
import com.example.demo.core.model.Product;

import java.util.List;

public class ProductConverter {

    public static List<ProductResponseDTO> toResponseDTO(List<Product> products){
        return products.stream()
                .map(product -> new ProductResponseDTO(
                        product.getId(),
                        product.getName(),
                        product.getDescription(),
                        product.getPrice(),
                        product.getImageUrl(),
                        product.getPreparationTime(),
                        product.getCategory().getName(),
                        product.getCreatedAt(),
                        product.getUpdatedAt()
                ))
                .toList();
    }
}
