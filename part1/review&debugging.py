# Assumes Flask + SQLAlchemy setup already exists

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    if not data.get('name') or not data.get('sku'):
        return {"error": "Required fields missing"}, 400

    if Product.query.filter_by(sku=data['sku']).first():
        return {"error": "SKU already exists"}, 409

    try:
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=Decimal(data['price']) if data.get('price') else None
        )

        db.session.add(product)
        db.session.flush()

        if data.get('warehouse_id') and data.get('initial_quantity') is not None:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=data['initial_quantity']
            )
            db.session.add(inventory)

        db.session.commit()
        return {"message": "Product created", "product_id": product.id}

    except Exception:
        db.session.rollback()
        return {"error": "Something went wrong"}, 500
