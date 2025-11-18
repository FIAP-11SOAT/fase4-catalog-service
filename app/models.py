from sqlalchemy import Column, DateTime, BigInteger, String, Text, Numeric, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from .db import Base


class Category(Base):
    __tablename__ = "product_categories"

    # Align with SQL: bigserial primary key
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(12, 2), nullable=False)
    image_url = Column(String(500), nullable=True)
    preparation_time = Column(Integer, nullable=False)
    category_id = Column(BigInteger, ForeignKey("product_categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship
    category = relationship("Category", back_populates="products")
