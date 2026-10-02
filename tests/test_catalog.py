from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
import models

client = TestClient(app)

def test_duplicate_sku_rejection():
    db = SessionLocal()
    cat = models.Category(name="Cat A", slug="cat-a")
    db.add(cat)
    db.commit()
    prod = models.Product(category_id=cat.id, name="Book A", slug="book-a")
    db.add(prod)
    db.commit()
    var = models.Variant(product_id=prod.id, option_values={"binding": "Paperback"})
    db.add(var)
    db.commit()
    sku = models.SKU(variant_id=var.id, sku_code="SKU-TEST-100", price=1000, stock_quantity=10)
    db.add(sku)
    db.commit()
    prod_id = prod.id
    db.close()

    payload = {
        "sku_code": "SKU-TEST-100", 
        "price": 2000,
        "stock_quantity": 5
    }
    response = client.post(f"/api/v1/admin/products/{prod_id}/skus", json=payload)
    assert response.status_code == 409

def test_negative_stock_rejection():
    db = SessionLocal()
    cat = models.Category(name="Cat B", slug="cat-b")
    db.add(cat)
    db.commit()
    prod = models.Product(category_id=cat.id, name="Book B", slug="book-b")
    db.add(prod)
    db.commit()
    var = models.Variant(product_id=prod.id, option_values={"binding": "Hardcover"})
    db.add(var)
    db.commit()
    sku = models.SKU(variant_id=var.id, sku_code="SKU-TEST-200", price=1500, stock_quantity=10)
    db.add(sku)
    db.commit()
    sku_id = sku.id
    db.close()

    payload = {"stock_quantity": -2}
    response = client.patch(f"/api/v1/admin/skus/{sku_id}", json=payload)
    assert response.status_code == 422