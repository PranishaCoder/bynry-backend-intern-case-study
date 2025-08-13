# part1_code_fix.py

from flask import request
from app import app, db  # assuming app and db are already created
from models import Product, Inventory  # assuming database models


@app.route('/api/products', methods=['POST'])
def create_product():
    """
    API endpoint to create a new product in the system
    - Validates input
    - Ensures SKU is unique
    - Handles optional fields
    - Supports linking product to warehouse inventory
    - Uses single transaction for data consistency
    """

    # 1. Get and validate request data
    data = request.get_json()

    # Check for mandatory fields
    required_fields = ['name', 'sku', 'price']
    for field in required_fields:
        if not data.get(field):
            return {"error": f"Missing required field: {field}"}, 400

    # Validate price
    try:
        price = float(data['price'])
    except (ValueError, TypeError):
        return {"error": "Price must be a valid number"}, 400

    # 2. Check SKU uniqueness
    existing_product = Product.query.filter_by(sku=data['sku']).first()
    if existing_product:
        return {
            "error": f"SKU '{data['sku']}' already exists for product '{existing_product.name}'"
        }, 409

    # 3. Create Product
    product = Product(
        name=data['name'],
        sku=data['sku'],
        price=price,
        description=data.get('description', '')  # Optional
    )

    try:
        db.session.add(product)
        db.session.flush()  # Get product.id before commit

        # 4. Add inventory
        if 'warehouses' in data:
            for wh in data['warehouses']:
                inventory = Inventory(
                    product_id=product.id,
                    warehouse_id=wh['id'],
                    quantity=wh.get('quantity', 0)
                )
                db.session.add(inventory)
        elif 'warehouse_id' in data:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=data.get('initial_quantity', 0)
            )
            db.session.add(inventory)

        # 5. Commit
        db.session.commit()

        return {
            "message": "Product created successfully",
            "product_id": product.id
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to create product: {str(e)}"}, 500
