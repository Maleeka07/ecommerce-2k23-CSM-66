# Sprint 2: Catalog Data Foundation

## 1. Sprint Goal and Scope Boundary
The objective of Sprint 2 is to build a robust catalog foundation for BookNook that accurately persists categories, products, variants, and SKUs without losing identity, relational integrity, pricing, or inventory meaning. 

**In Scope:**
* Category tree management (with stable slugs and self-ancestor prevention).
* Product creation (including title, slug, status, and descriptive content).
* Variant and SKU records (unique codes, individual pricing, and stock tracking).
* Authenticated administrative endpoints for CRUD operations.
* Database migrations, constraints, seed data, and automated tests.

**Out of Scope:**
Public catalog search, asset upload functionality, dynamic specifications workflows, and integration with payment gateways or shipping logic are deferred to Sprint 3 or later.

## 2. Link to Sprint 1 Decisions
To fulfill the mandatory Catalog standard of Products, Variants, and SKUs, the original Sprint 1 `LISTINGS` concept has been refactored:
* **Reused Decisions:** The Next.js frontend, FastAPI backend, and PostgreSQL database stack remain unchanged. The platform continues to serve the independent and used bookstore vertical.
* **Changes & Adaptations:** Sprint 1 originally modeled used books as single-copy `LISTINGS` with an `is_available` boolean. To satisfy Sprint 2 requirements, `LISTINGS` is split into `PRODUCTS` (the core book), `VARIANTS` (the edition/format), and `SKUS` (the physical stock level and condition). 
* **Pricing Mechanism:** Floating-point money has been rejected. Prices on the `SKUS` table are stored as integer minor units (cents) to prevent rounding errors. 

## 3. Updated ERD and Data Dictionary
The schema has been extended from the Sprint 1 MVP to map the core catalog entities securely to the previously established cart and order tables.

**Data Dictionary & Integrity Policies:**
* **Categories:** `id` (PK), `parent_id` (FK to Categories, ON DELETE SET NULL), `name`, `slug` (UNIQUE), `active_status`.
* **Products:** `id` (PK), `category_id` (FK, ON DELETE RESTRICT), `name`, `slug` (UNIQUE), `description`, `status`, `specifications` (JSON).
* **Variants:** `id` (PK), `product_id` (FK, ON DELETE CASCADE), `option_values` (JSON).
* **SKUs:** `id` (PK), `variant_id` (FK, ON DELETE CASCADE), `sku_code` (UNIQUE), `price` (INTEGER cents), `stock_quantity` (CHECK >= 0), `active_status`.
* **Assets:** `id` (PK), `entity_type` (Enum), `entity_id` (FK), `storage_url`, `alt_text`, `sort_order`.

```mermaid
erDiagram
    CATEGORIES ||--o{ PRODUCTS: contains
    CATEGORIES ||--o{ CATEGORIES: parent
    PRODUCTS ||--o{ VARIANTS: has
    PRODUCTS ||--o{ ASSETS: displays
    VARIANTS ||--o{ SKUS: materializes
    VARIANTS ||--o{ ASSETS: displays
    SKUS ||--o{ CART_ITEMS: selected_as
    SKUS ||--o{ ORDER_ITEMS: sold_as

    CATEGORIES {
        int id PK
        int parent_id FK
        string name
        string slug
        boolean active_status
    }
    PRODUCTS {
        int id PK
        int category_id FK
        string name
        string slug
        string description
        json specifications
        string status
    }
    VARIANTS {
        int id PK
        int product_id FK
        json option_values
    }
    SKUS {
        int id PK
        int variant_id FK
        string sku_code
        int price
        int stock_quantity
        boolean active_status
    }
