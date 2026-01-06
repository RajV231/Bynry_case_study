# Database Design

## Tables

**companies**
- id (PK)
- name

**warehouses**
- id (PK)
- company_id (FK)
- name
- location

**products**
- id (PK)
- company_id (FK)
- name
- sku (UNIQUE)
- price (DECIMAL)
- product_type

**inventory**
- id (PK)
- product_id (FK)
- warehouse_id (FK)
- quantity
- updated_at

**inventory_logs**
- id (PK)
- inventory_id (FK)
- change_amount
- created_at

**suppliers**
- id (PK)
- name
- contact_email

**product_suppliers**
- product_id (FK)
- supplier_id (FK)

**product_bundles**
- bundle_id (FK → products)
- child_product_id (FK → products)
- quantity

## Design Notes
- Inventory is separated from products to support multiple warehouses.
- Inventory logs track stock changes.
- Many-to-many tables support suppliers and bundles.
