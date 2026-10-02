from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class CategoryCreate(BaseModel):
    name: str
    slug: str
    parent_id: Optional[int] = None
    active_status: Optional[bool] = True

class ProductCreate(BaseModel):
    category_id: int
    name: str
    slug: str
    description: Optional[str] = None
    status: Optional[str] = "draft"
    specifications: Optional[Dict[str, Any]] = None

class SKUCreate(BaseModel):
    sku_code: str
    price: int = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    active_status: Optional[bool] = True

class SKUUpdate(BaseModel):
    price: Optional[int] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    active_status: Optional[bool] = None