from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..db import get_db
from ..models import Product as ProductModel, Category as CategoryModel
from ..schemas import ProductInput, ProductResponse
from ..security import require_admin


router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[ProductResponse])
def list_all_products(
    category_id: Optional[int] = Query(None, description="Filtrar por categoria"),
    db: Session = Depends(get_db)
):
    query = db.query(ProductModel)
    
    if category_id is not None:
        query = query.filter(ProductModel.category_id == category_id)
    
    rows = query.order_by(ProductModel.id.asc()).all()
    
    if len(rows) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])
    
    return rows


@router.get("/{product_id}", response_model=ProductResponse)
def find_product_by_id(product_id: int, db: Session = Depends(get_db)):
    row = db.get(ProductModel, product_id)
    if row is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])
    return row


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(
    payload: ProductInput,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    # Validar se a categoria existe
    category = db.get(CategoryModel, payload.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with id {payload.category_id} does not exist"
        )
    
    row = ProductModel(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        image_url=payload.image_url,
        preparation_time=payload.preparation_time,
        category_id=payload.category_id
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Unique violation on name -> 409 Conflict
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product name already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    db.refresh(row)
    return row


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductInput,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    row = db.get(ProductModel, product_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Validar se a categoria existe
    category = db.get(CategoryModel, payload.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with id {payload.category_id} does not exist"
        )

    row.name = payload.name
    row.description = payload.description
    row.price = payload.price
    row.image_url = payload.image_url
    row.preparation_time = payload.preparation_time
    row.category_id = payload.category_id
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product name already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    db.refresh(row)
    return row


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    row = db.get(ProductModel, product_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(row)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
