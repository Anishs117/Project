Vendor Management System with Performance Metrics

Objective
Develop a Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

Technologies
Django
Django REST Framework
MySQL
Swagger (for testing)

Core Features
1. Vendor Profile Management
Model Design: Create a model to store vendor information including name, contact details, address, and a unique vendor code.
API Endpoints:
POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
PUT /api/vendors/{vendor_id}/: Update a vendor's details.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.
2. Purchase Order Tracking
Model Design: Track purchase orders with fields like PO number, vendor reference, order date, items, quantity, and status.
API Endpoints:
POST /api/purchase_orders/: Create a purchase order.
GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase_orders/{po_id}/: Update a purchase order.
DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
3. Vendor Performance Evaluation
Metrics:
On-Time Delivery Rate: Percentage of orders delivered by the promised date.
Quality Rating: Average of quality ratings given to a vendor’s purchase orders.
Response Time: Average time taken by a vendor to acknowledge or respond to purchase orders.
Fulfilment Rate: Percentage of purchase orders fulfilled without issues.
Model Design: Add fields to the vendor model to store these performance metrics.
API Endpoints:
GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics.

Installation
Clone the repository.
Install dependencies using pip install -r requirements.txt.
Run migrations using python manage.py migrate.
Start the server using python manage.py runserver.

Usage
Access the Swagger UI for API documentation and testing at http://localhost:8000/swagger/.