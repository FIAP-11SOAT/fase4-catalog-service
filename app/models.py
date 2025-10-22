from sqlalchemy import Column, DateTime, BigInteger, String, Text, func
from .db import Base


class Category(Base):
    __tablename__ = "product_categories"

    # Align with SQL: bigserial primary key
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
