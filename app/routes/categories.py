from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..db import get_db
from ..models import Category as CategoryModel
from ..schemas import CategoryInput, CategoryResponse
from ..security import require_admin


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=List[CategoryResponse])
def list_all_categories(db: Session = Depends(get_db)):
    rows = db.query(CategoryModel).order_by(CategoryModel.id.asc()).all()
    if len(rows) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])
    return rows


@router.get("/{category_id}", response_model=CategoryResponse)
def find_category_by_id(category_id: int, db: Session = Depends(get_db)):
    row = db.get(CategoryModel, category_id)
    if row is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])
    return row


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def create_category(
    payload: CategoryInput,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    row = CategoryModel(name=payload.name, description=payload.description)
    db.add(row)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Unique violation on name -> 409 Conflict
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category name already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    db.refresh(row)
    return row


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    payload: CategoryInput,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    row = db.get(CategoryModel, category_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    row.name = payload.name
    row.description = payload.description
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category name already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    db.refresh(row)
    return row


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    row = db.get(CategoryModel, category_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(row)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
