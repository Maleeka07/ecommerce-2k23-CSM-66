from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])

@router.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Category).filter(models.Category.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=409, detail="Duplicate Category Slug")
    category = models.Category(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Product).filter(models.Product.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=409, detail="Duplicate Product Slug")
    product = models.Product(**payload.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.post("/products/{product_id}/skus", status_code=status.HTTP_201_CREATED)
def create_sku(product_id: int, payload: schemas.SKUCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_sku = db.query(models.SKU).filter(models.SKU.sku_code == payload.sku_code).first()
    if existing_sku:
        raise HTTPException(status_code=409, detail="Duplicate SKU Code")
    
    # Ensure variant exists or create default variant for product
    variant = db.query(models.Variant).filter(models.Variant.product_id == product_id).first()
    if not variant:
        variant = models.Variant(product_id=product_id, option_values={"format": "Standard"})
        db.add(variant)
        db.commit()
        db.refresh(variant)

    sku = models.SKU(variant_id=variant.id, **payload.dict())
    db.add(sku)
    db.commit()
    db.refresh(sku)
    return sku

@router.patch("/skus/{sku_id}")
def update_sku(sku_id: int, payload: schemas.SKUUpdate, db: Session = Depends(get_db)):
    sku = db.query(models.SKU).filter(models.SKU.id == sku_id).first()
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    
    if payload.stock_quantity is not None and payload.stock_quantity < 0:
        raise HTTPException(status_code=422, detail="Stock cannot be negative")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sku, key, value)
    
    db.commit()
    db.refresh(sku)
    return sku