from database import SessionLocal, engine, Base
import models

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    cat1 = models.Category(name="Fiction", slug="fiction")
    db.add(cat1)
    db.commit()

    prod = models.Product(category_id=cat1.id, name="Dune", slug="dune", status="published")
    db.add(prod)
    db.commit()

    variant = models.Variant(product_id=prod.id, option_values={"binding": "Hardcover"})
    db.add(variant)
    db.commit()

    sku = models.SKU(variant_id=variant.id, sku_code="DUNE-HC-G", price=3000, stock_quantity=5)
    db.add(sku)
    db.commit()

    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()