# Assumes existing models and database setup

@app.route('/api/companies/<int:company_id>/alerts/low-stock')
def low_stock_alerts(company_id):
    alerts = []

    records = (
        db.session.query(Inventory, Product, Warehouse, Supplier)
        .join(Product)
        .join(Warehouse)
        .join(ProductSupplier)
        .join(Supplier)
        .filter(Warehouse.company_id == company_id)
        .all()
    )

    for inv, product, warehouse, supplier in records:
        if inv.quantity < product.low_stock_threshold and product.has_recent_sales:
            days_left = inv.quantity / product.avg_daily_sales

            alerts.append({
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "warehouse_id": warehouse.id,
                "warehouse_name": warehouse.name,
                "current_stock": inv.quantity,
                "threshold": product.low_stock_threshold,
                "days_until_stockout": int(days_left),
                "supplier": {
                    "id": supplier.id,
                    "name": supplier.name,
                    "contact_email": supplier.contact_email
                }
            })

    return {
        "alerts": alerts,
        "total_alerts": len(alerts)
    }
