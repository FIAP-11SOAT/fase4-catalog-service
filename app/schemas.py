from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class CategoryInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ProductInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0, decimal_places=2)
    image_url: Optional[str] = Field(None, max_length=500)
    preparation_time: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    preparation_time: int
    category_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
