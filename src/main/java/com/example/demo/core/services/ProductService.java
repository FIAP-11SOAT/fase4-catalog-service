package com.example.demo.core.services;

import com.example.demo.adapters.dto.ProductRequestDTO;
import com.example.demo.adapters.outbound.repository.ProductRepositoryPort;
import com.example.demo.core.model.Category;
import com.example.demo.core.model.Product;
import com.example.demo.core.port.CategoryServicePort;
import com.example.demo.core.port.ProductServicePort;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ProductService implements ProductServicePort {

    private final ProductRepositoryPort productRepository;
    private final CategoryServicePort categoryService;

    public ProductService(ProductRepositoryPort productRepository, CategoryServicePort categoryService) {
        this.productRepository = productRepository;
        this.categoryService = categoryService;
    }

    @Override
    public List<Product> getAll(Long categoryId) {

        if (categoryId != null){
            Category category = categoryService.getById(categoryId);
            return productRepository.findByCategory(category);
        }
        return productRepository.findAll();
    }

    @Override
    public Product getById(Long id) {
        Optional<Product> product = productRepository.findById(id);
        return product.orElse(null);
    }

    @Override
    public Product create(ProductRequestDTO productRequestDTO) {
        Category category = categoryService.getById(productRequestDTO.categoryId());
        Product product = createProduct(productRequestDTO, category);
        return productRepository.save(product);
    }

    @Override
    public Product update(Long id, ProductRequestDTO productRequestDTO) {
        Category category = categoryService.getById(productRequestDTO.categoryId());
        Product product = getById(id);
        if (product == null){
            throw new RuntimeException("O produto não existe");
        }
        Product updatedProduct = updateProduct(product, productRequestDTO, category);
        return productRepository.save(updatedProduct);
    }

    @Override
    public void delete(Long id) {
        productRepository.deleteById(id);
    }

    private Product createProduct(ProductRequestDTO dto, Category category) {
        Product product = new Product();

        product.setName(dto.name().trim());
        product.setDescription(dto.description());
        product.setPrice(dto.price());
        product.setImageUrl(dto.imageUrl());
        product.setPreparationTime(dto.preparationTime());
        product.setCategory(category);

        return product;
    }

    private Product updateProduct(Product product, ProductRequestDTO dto, Category category){
        product.setName(dto.name().trim());
        product.setDescription(dto.description());
        product.setPrice(dto.price());
        product.setImageUrl(dto.imageUrl());
        product.setPreparationTime(dto.preparationTime());
        product.setCategory(category);

        return product;
    }
}
