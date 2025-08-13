# part3_low_stock_api.py

from flask import request
from datetime import datetime, timedelta
from app import app, db
from models import Product, Warehouse, Inventory, Supplier, Supplier_Product, Inventory_Transactions

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    """
    Returns low-stock alerts for a given company.
    - Low stock threshold varies per product
    - Only alert for products with recent sales (last 30 days)
    - Supports multiple warehouses
    - Includes supplier info
    """
    try:
        recent_cutoff = datetime.now() - timedelta(days=30)

        results = (
            db.session.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Product.sku,
                Warehouse.id.label("warehouse_id"),
                Warehouse.name.label("warehouse_name"),
                Inventory.quantity.label("current_stock"),
                Product.low_stock_threshold.label("threshold")
            )
            .join(Inventory, Product.id == Inventory.product_id)
            .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
            .filter(Product.company_id == company_id)
            .filter(Product.active == True)
            .filter(Warehouse.company_id == company_id)
            .all()
        )

        alerts = []

        for row in results:
            avg_daily_sales = (
                db.session.query(
                    db.func.coalesce(
                        db.func.sum(Inventory_Transactions.change_qty * -1), 0
                    ) / 30.0
                )
                .join(Inventory, Inventory_Transactions.inventory_id == Inventory.id)
                .filter(Inventory.product_id == row.product_id)
                .filter(Inventory_Transactions.created_at >= recent_cutoff)
                .filter(Inventory_Transactions.change_qty < 0)
                .scalar()
            )

            if avg_daily_sales == 0:
                continue

            if row.current_stock < (row.threshold or 0):
                days_until_stockout = None
                if avg_daily_sales > 0:
                    days_until_stockout = int(row.current_stock / avg_daily_sales)

                supplier_info = (
                    db.session.query(Supplier)
                    .join(Supplier_Product, Supplier.id == Supplier_Product.supplier_id)
                    .filter(Supplier_Product.product_id == row.product_id)
                    .first()
                )

                supplier_data = None
                if supplier_info:
                    supplier_data = {
                        "id": supplier_info.id,
                        "name": supplier_info.name,
                        "contact_email": supplier_info.contact_email
                    }

                alerts.append({
                    "product_id": row.product_id,
                    "product_name": row.product_name,
                    "sku": row.sku,
                    "warehouse_id": row.warehouse_id,
                    "warehouse_name": row.warehouse_name,
                    "current_stock": row.current_stock,
                    "threshold": row.threshold,
                    "days_until_stockout": days_until_stockout,
                    "supplier": supplier_data
                })

        return {
            "alerts": alerts,
            "total_alerts": len(alerts)
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500
