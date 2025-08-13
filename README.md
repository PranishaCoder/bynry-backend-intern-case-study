```markdown
# Bynry Backend Intern – Case Study Submission

This repository contains my completed case study for the **Backend Developer Intern** role at **Bynry Inc**.  
It includes solutions for **Code Review & Debugging**, **Database Design**, and **API Implementation**.

---

## 📂 Repository Structure

```

.
├── part1\_code\_fix.py         # Fixed API endpoint for product creation
├── part2\_schema.sql          # Database schema (DDL) for StockFlow
├── part3\_low\_stock\_api.py    # Low-stock alerts API implementation
└── Pranisha\_Pol\_Task.pdf     # Documented answers (optional reference)

```

---

## 📜 Part 1 – Code Review & Debugging

**File:** `part1_code_fix.py`  
- Fixed technical and business logic issues in the given product creation API.
- Improvements include:
  - SKU uniqueness check
  - Multiple warehouse support
  - Input validation
  - Decimal price handling
  - Optional field handling
  - Single transaction for consistency
  - Proper error handling and rollback

---

## 🗄️ Part 2 – Database Design

**File:** `part2_schema.sql`  
- Designed a relational database schema for **StockFlow**, a B2B inventory management system.
- Key features:
  - Support for multiple warehouses per company
  - Inventory transactions for stock movement tracking
  - Supplier-product many-to-many relationship
  - Product bundles support
  - Soft delete for products
  - Proper indexes, unique constraints, and foreign keys

---

## ⚙️ Part 3 – Low Stock Alerts API

**File:** `part3_low_stock_api.py`  
- **API endpoint:**
```

GET /api/companies/\<company\_id>/alerts/low-stock

````
- Features:
- Low stock threshold per product
- Alerts only for products with recent sales (last 30 days)
- Multi-warehouse support
- Supplier information included for reordering
- Days until stock-out calculation
- Handles missing thresholds, zero sales, and no suppliers gracefully

---

## 🚀 How to Run

### 1️⃣ Requirements
- Python 3.x
- Flask
- SQLAlchemy
- A configured database (MySQL/PostgreSQL/etc.)

### 2️⃣ Install dependencies
```bash
pip install flask sqlalchemy
````

### 3️⃣ Run the API

* Add your database configuration in `app.py` (Flask app initialization).
* Run:

```bash
flask run
```

### 4️⃣ Test Endpoints

Use Postman or curl to test:

```bash
curl http://localhost:5000/api/companies/1/alerts/low-stock
```

---

## 👩‍💻 Author

**Pranisha Dhananjay Pol**

* BE in Artificial Intelligence & Data Science
* Passionate about backend development, data analytics, and scalable API design.

---

## 📌 Notes

* This repo contains both runnable code and the documented approach (`Pranisha_Pol_Task.pdf`) for reference.
* The APIs assume a working database with tables from `part2_schema.sql`.

```
```
