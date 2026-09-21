# DataTalk Evaluation Report

## Generated

2026-09-21T21:26:42.130366+00:00

## General Metrics

| Metric | Score |
|---|---:|
| Total Questions | 45 |
| Text-to-SQL Accuracy | 8.89% |
| Execution Accuracy | 53.33% |
| Retry Success Rate | 0.00% |
| First Pass Accuracy | 53.33% |
| Average Retry Count | 0.00 |

## Failed Cases

### Case agg_001

**Question:** How many orders does each customer have?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT c.customer_id, c.company_name, COUNT(o.order_id) AS total_orders FROM customers AS c JOIN orders AS o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.company_name ORDER BY c.company_name
```

**Expected SQL:**

```sql
SELECT customer_id, COUNT(order_id) FROM orders GROUP BY customer_id
```

**Expected Rows:**

Showing first 5 of 89 rows.

```json
[
  {
    "customer_id": "TOMSP",
    "count": 6
  },
  {
    "customer_id": "LONEP",
    "count": 8
  },
  {
    "customer_id": "OLDWO",
    "count": 10
  },
  {
    "customer_id": "WARTH",
    "count": 15
  },
  {
    "customer_id": "MAGAA",
    "count": 10
  }
]
```

**Generated Rows:**

Showing first 5 of 89 rows.

```json
[
  {
    "customer_id": "ALFKI",
    "company_name": "Alfreds Futterkiste",
    "total_orders": 6
  },
  {
    "customer_id": "ANATR",
    "company_name": "Ana Trujillo Emparedados y helados",
    "total_orders": 4
  },
  {
    "customer_id": "ANTON",
    "company_name": "Antonio Moreno Taquería",
    "total_orders": 7
  },
  {
    "customer_id": "AROUT",
    "company_name": "Around the Horn",
    "total_orders": 13
  },
  {
    "customer_id": "BSBEV",
    "company_name": "B's Beverages",
    "total_orders": 10
  }
]
```

**Error:** None

### Case agg_002

**Question:** What is the average product price?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT AVG(unit_price) AS average_product_price FROM products
```

**Expected SQL:**

```sql
SELECT AVG(unit_price) FROM products
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "avg": 28.83389609200614
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "average_product_price": 28.83389609200614
  }
]
```

**Error:** None

### Case agg_003

**Question:** What is the total number of products per category?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT c.category_name, COUNT(p.product_id) AS total_products FROM categories AS c JOIN products AS p ON c.category_id = p.category_id GROUP BY c.category_name ORDER BY c.category_name
```

**Expected SQL:**

```sql
SELECT category_id, COUNT(product_id) FROM products GROUP BY category_id
```

**Expected Rows:**

Showing first 5 of 8 rows.

```json
[
  {
    "category_id": 8,
    "count": 12
  },
  {
    "category_id": 7,
    "count": 5
  },
  {
    "category_id": 1,
    "count": 12
  },
  {
    "category_id": 5,
    "count": 7
  },
  {
    "category_id": 4,
    "count": 10
  }
]
```

**Generated Rows:**

Showing first 5 of 8 rows.

```json
[
  {
    "category_name": "Beverages",
    "total_products": 12
  },
  {
    "category_name": "Condiments",
    "total_products": 12
  },
  {
    "category_name": "Confections",
    "total_products": 13
  },
  {
    "category_name": "Dairy Products",
    "total_products": 10
  },
  {
    "category_name": "Grains/Cereals",
    "total_products": 7
  }
]
```

**Error:** None

### Case agg_004

**Question:** Calculate the total sales amount.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT SUM(unit_price * quantity * (1 - discount)) AS total_sales_amount FROM order_details
```

**Expected SQL:**

```sql
SELECT SUM(unit_price * quantity) FROM order_details
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "sum": 1354458.590441227
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "total_sales_amount": 1265793.038653364
  }
]
```

**Error:** None

### Case agg_005

**Question:** Find the maximum product price.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT MAX(unit_price) AS maximum_product_price FROM products
```

**Expected SQL:**

```sql
SELECT MAX(unit_price) FROM products
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "max": 263.5
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "maximum_product_price": 263.5
  }
]
```

**Error:** None

### Case agg_006

**Question:** Find the cheapest product price.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT MIN(unit_price) AS minimum_price FROM products
```

**Expected SQL:**

```sql
SELECT MIN(unit_price) FROM products
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "min": 2.5
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "minimum_price": 2.5
  }
]
```

**Error:** None

### Case agg_007

**Question:** How many employees work in each city?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT city, COUNT(employee_id) AS total_employees FROM employees GROUP BY city
```

**Expected SQL:**

```sql
SELECT city, COUNT(employee_id) FROM employees GROUP BY city
```

**Expected Rows:**

Showing 5 of 5 rows.

```json
[
  {
    "city": "Redmond",
    "count": 1
  },
  {
    "city": "London",
    "count": 4
  },
  {
    "city": "Tacoma",
    "count": 1
  },
  {
    "city": "Kirkland",
    "count": 1
  },
  {
    "city": "Seattle",
    "count": 2
  }
]
```

**Generated Rows:**

Showing 5 of 5 rows.

```json
[
  {
    "city": "Redmond",
    "total_employees": 1
  },
  {
    "city": "London",
    "total_employees": 4
  },
  {
    "city": "Tacoma",
    "total_employees": 1
  },
  {
    "city": "Kirkland",
    "total_employees": 1
  },
  {
    "city": "Seattle",
    "total_employees": 2
  }
]
```

**Error:** None

### Case agg_008

**Question:** What is the average number of units in stock?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT AVG(units_in_stock) AS average_units_in_stock FROM products
```

**Expected SQL:**

```sql
SELECT AVG(units_in_stock) FROM products
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "avg": 40.506493506493506
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "average_units_in_stock": 40.506493506493506
  }
]
```

**Error:** None

### Case agg_009

**Question:** Show total orders per year.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT EXTRACT(YEAR FROM order_date) AS order_year, COUNT(order_id) AS total_orders FROM orders GROUP BY order_year ORDER BY order_year
```

**Expected SQL:**

```sql
SELECT YEAR(order_date), COUNT(order_id) FROM orders GROUP BY YEAR(order_date)
```

**Expected Rows:**

Showing 0 of 0 rows.

```json
[]
```

**Generated Rows:**

Showing 3 of 3 rows.

```json
[
  {
    "order_year": 1996.0,
    "total_orders": 152
  },
  {
    "order_year": 1997.0,
    "total_orders": 408
  },
  {
    "order_year": 1998.0,
    "total_orders": 270
  }
]
```

**Error:** None

### Case agg_010

**Question:** Which category contains the most products?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT c.category_name, COUNT(p.product_id) AS product_count FROM categories AS c JOIN products AS p ON c.category_id = p.category_id GROUP BY c.category_name ORDER BY product_count DESC LIMIT 1
```

**Expected SQL:**

```sql
SELECT category_id, COUNT(product_id) FROM products GROUP BY category_id ORDER BY COUNT(product_id) DESC LIMIT 1
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "category_id": 3,
    "count": 13
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "category_name": "Confections",
    "product_count": 13
  }
]
```

**Error:** None

### Case basic_001

**Question:** How many customers are there?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT COUNT(customer_id) AS total_customers FROM customers
```

**Expected SQL:**

```sql
SELECT COUNT(customer_id) FROM customers
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "count": 91
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "total_customers": 91
  }
]
```

**Error:** None

### Case basic_002

**Question:** How many products exist?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT COUNT(*) AS total_products FROM products
```

**Expected SQL:**

```sql
SELECT COUNT(product_id) FROM products
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "count": 77
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "total_products": 77
  }
]
```

**Error:** None

### Case basic_003

**Question:** List all customer company names.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT company_name AS company_name FROM customers
```

**Expected SQL:**

```sql
SELECT company_name FROM customers
```

**Expected Rows:**

Showing first 5 of 91 rows.

```json
[
  {
    "company_name": "Alfreds Futterkiste"
  },
  {
    "company_name": "Ana Trujillo Emparedados y helados"
  },
  {
    "company_name": "Antonio Moreno Taquería"
  },
  {
    "company_name": "Around the Horn"
  },
  {
    "company_name": "Berglunds snabbköp"
  }
]
```

**Generated Rows:**

Showing first 5 of 91 rows.

```json
[
  {
    "company_name": "Alfreds Futterkiste"
  },
  {
    "company_name": "Ana Trujillo Emparedados y helados"
  },
  {
    "company_name": "Antonio Moreno Taquería"
  },
  {
    "company_name": "Around the Horn"
  },
  {
    "company_name": "Berglunds snabbköp"
  }
]
```

**Error:** None

### Case basic_004

**Question:** Show all categories.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT * FROM categories
```

**Expected SQL:**

```sql
SELECT category_name FROM categories
```

**Expected Rows:**

Showing first 5 of 8 rows.

```json
[
  {
    "category_name": "Beverages"
  },
  {
    "category_name": "Condiments"
  },
  {
    "category_name": "Confections"
  },
  {
    "category_name": "Dairy Products"
  },
  {
    "category_name": "Grains/Cereals"
  }
]
```

**Generated Rows:**

Showing first 5 of 8 rows.

```json
[
  {
    "category_id": 1,
    "category_name": "Beverages",
    "description": "Soft drinks, coffees, teas, beers, and ales",
    "picture": ""
  },
  {
    "category_id": 2,
    "category_name": "Condiments",
    "description": "Sweet and savory sauces, relishes, spreads, and seasonings",
    "picture": ""
  },
  {
    "category_id": 3,
    "category_name": "Confections",
    "description": "Desserts, candies, and sweet breads",
    "picture": ""
  },
  {
    "category_id": 4,
    "category_name": "Dairy Products",
    "description": "Cheeses",
    "picture": ""
  },
  {
    "category_id": 5,
    "category_name": "Grains/Cereals",
    "description": "Breads, crackers, pasta, and cereal",
    "picture": ""
  }
]
```

**Error:** None

### Case basic_005

**Question:** How many orders exist?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT COUNT(*) AS total_orders FROM orders
```

**Expected SQL:**

```sql
SELECT COUNT(order_id) FROM orders
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "count": 830
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "total_orders": 830
  }
]
```

**Error:** None

### Case complex_001

**Question:** Who is the customer with the highest number of orders?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT c.company_name, COUNT(o.order_id) AS order_count FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id ORDER BY order_count DESC LIMIT 1
```

**Expected SQL:**

```sql
SELECT customer_id, COUNT(order_id) AS total_orders FROM orders GROUP BY customer_id ORDER BY total_orders DESC LIMIT 1
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "customer_id": "SAVEA",
    "total_orders": 31
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "company_name": "Save-a-lot Markets",
    "order_count": 31
  }
]
```

**Error:** None

### Case complex_002

**Question:** What is the best selling product?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT p.product_name, SUM(od.quantity * od.unit_price * (1 - od.discount)) AS total_sales FROM order_details od JOIN products p ON od.product_id = p.product_id GROUP BY p.product_id, p.product_name ORDER BY total_sales DESC LIMIT 1
```

**Expected SQL:**

```sql
SELECT product_id, SUM(quantity) AS total_quantity FROM order_details GROUP BY product_id ORDER BY total_quantity DESC LIMIT 1
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "product_id": 60,
    "total_quantity": 1577
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "product_name": "Côte de Blaye",
    "total_sales": 141396.7356273254
  }
]
```

**Error:** None

### Case complex_003

**Question:** Find categories with average product price above 30.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT c.category_name, AVG(p.unit_price) AS average_price FROM products p JOIN categories c ON p.category_id = c.category_id GROUP BY c.category_id HAVING AVG(p.unit_price) > 30
```

**Expected SQL:**

```sql
SELECT category_id, AVG(unit_price) FROM products GROUP BY category_id HAVING AVG(unit_price) > 30
```

**Expected Rows:**

Showing 3 of 3 rows.

```json
[
  {
    "category_id": 7,
    "avg": 32.369999694824216
  },
  {
    "category_id": 1,
    "avg": 37.979166666666664
  },
  {
    "category_id": 6,
    "avg": 54.00666666030884
  }
]
```

**Generated Rows:**

Showing 3 of 3 rows.

```json
[
  {
    "category_name": "Produce",
    "average_price": 32.369999694824216
  },
  {
    "category_name": "Beverages",
    "average_price": 37.979166666666664
  },
  {
    "category_name": "Meat/Poultry",
    "average_price": 54.00666666030884
  }
]
```

**Error:** None

### Case complex_004

**Question:** Which employee generated the highest sales?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT e.last_name, e.first_name, SUM(od.total_order_value) AS total_sales FROM orders o JOIN (SELECT order_id, SUM(unit_price * quantity * (1 - discount)) AS total_order_value FROM order_details GROUP BY order_id) od ON o.order_id = od.order_id JOIN employees e ON o.employee_id = e.employee_id GROUP BY e.employee_id ORDER BY total_sales DESC LIMIT 1
```

**Expected SQL:**

```sql
SELECT employees.employee_id, SUM(order_details.unit_price * order_details.quantity) AS sales FROM employees JOIN orders ON employees.employee_id = orders.employee_id JOIN order_details ON orders.order_id = order_details.order_id GROUP BY employees.employee_id ORDER BY sales DESC LIMIT 1
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "employee_id": 4,
    "sales": 250187.4502530098
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "last_name": "Peacock",
    "first_name": "Margaret",
    "total_sales": 232890.84598203754
  }
]
```

**Error:** None

### Case complex_005

**Question:** Find customers who never placed an order.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT customers.* FROM customers LEFT JOIN orders ON customers.customer_id = orders.customer_id WHERE orders.order_id IS NULL
```

**Expected SQL:**

```sql
SELECT customers.company_name FROM customers LEFT JOIN orders ON customers.customer_id = orders.customer_id WHERE orders.order_id IS NULL
```

**Expected Rows:**

Showing 2 of 2 rows.

```json
[
  {
    "company_name": "Paris spécialités"
  },
  {
    "company_name": "FISSA Fabrica Inter. Salchichas S.A."
  }
]
```

**Generated Rows:**

Showing 2 of 2 rows.

```json
[
  {
    "customer_id": "PARIS",
    "company_name": "Paris spécialités",
    "contact_name": "Marie Bertrand",
    "contact_title": "Owner",
    "address": "265, boulevard Charonne",
    "city": "Paris",
    "region": null,
    "postal_code": "75012",
    "country": "France",
    "phone": "(1) 42.34.22.66",
    "fax": "(1) 42.34.22.77"
  },
  {
    "customer_id": "FISSA",
    "company_name": "FISSA Fabrica Inter. Salchichas S.A.",
    "contact_name": "Diego Roel",
    "contact_title": "Accounting Manager",
    "address": "C/ Moralzarzal, 86",
    "city": "Madrid",
    "region": null,
    "postal_code": "28034",
    "country": "Spain",
    "phone": "(91) 555 94 44",
    "fax": "(91) 555 55 93"
  }
]
```

**Error:** None

### Case complex_006

**Question:** What products have never been ordered?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT products.product_id AS product_id, products.product_name AS product_name FROM products LEFT JOIN order_details ON products.product_id = order_details.product_id WHERE order_details.product_id IS NULL
```

**Expected SQL:**

```sql
SELECT products.product_name FROM products LEFT JOIN order_details ON products.product_id = order_details.product_id WHERE order_details.order_id IS NULL
```

**Expected Rows:**

Showing 0 of 0 rows.

```json
[]
```

**Generated Rows:**

Showing 0 of 0 rows.

```json
[]
```

**Error:** None

### Case complex_007

**Question:** Show monthly revenue.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT EXTRACT(MONTH FROM o.order_date) AS month, SUM(od.unit_price * od.quantity * (1 - od.discount)) AS total_revenue FROM orders o JOIN order_details od ON o.order_id = od.order_id GROUP BY EXTRACT(MONTH FROM o.order_date)
```

**Expected SQL:**

```sql
SELECT MONTH(order_date), SUM(unit_price * quantity) FROM orders JOIN order_details ON orders.order_id = order_details.order_id GROUP BY MONTH(order_date)
```

**Expected Rows:**

Showing 0 of 0 rows.

```json
[]
```

**Generated Rows:**

Showing first 5 of 12 rows.

```json
[
  {
    "month": 3.0,
    "total_revenue": 143401.37510988378
  },
  {
    "month": 7.0,
    "total_revenue": 78882.75264826637
  },
  {
    "month": 11.0,
    "total_revenue": 89133.85397870214
  },
  {
    "month": 4.0,
    "total_revenue": 176831.6346444887
  },
  {
    "month": 6.0,
    "total_revenue": 36362.80233480245
  }
]
```

**Error:** None

### Case complex_009

**Question:** Which countries generate the highest number of orders?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT c.country, COUNT(o.order_id) AS total_orders FROM orders o JOIN customers c ON o.customer_id = c.customer_id GROUP BY c.country ORDER BY total_orders DESC
```

**Expected SQL:**

```sql
SELECT ship_country, COUNT(order_id) FROM orders GROUP BY ship_country ORDER BY COUNT(order_id) DESC
```

**Expected Rows:**

Showing first 5 of 21 rows.

```json
[
  {
    "ship_country": "Germany",
    "count": 122
  },
  {
    "ship_country": "USA",
    "count": 122
  },
  {
    "ship_country": "Brazil",
    "count": 83
  },
  {
    "ship_country": "France",
    "count": 77
  },
  {
    "ship_country": "UK",
    "count": 56
  }
]
```

**Generated Rows:**

Showing first 5 of 21 rows.

```json
[
  {
    "country": "Germany",
    "total_orders": 122
  },
  {
    "country": "USA",
    "total_orders": 122
  },
  {
    "country": "Brazil",
    "total_orders": 83
  },
  {
    "country": "France",
    "total_orders": 77
  },
  {
    "country": "UK",
    "total_orders": 56
  }
]
```

**Error:** None

### Case complex_010

**Question:** What is the average order value?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT AVG(total_amount) AS average_order_value FROM (SELECT SUM(unit_price * quantity * (1 - discount)) AS total_amount FROM order_details GROUP BY order_id) AS order_totals
```

**Expected SQL:**

```sql
SELECT AVG(total) FROM (SELECT order_id, SUM(unit_price * quantity) AS total FROM order_details GROUP BY order_id)
```

**Expected Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "avg": 1631.8778198087073
  }
]
```

**Generated Rows:**

Showing 1 of 1 rows.

```json
[
  {
    "average_order_value": 1525.0518537992339
  }
]
```

**Error:** None

### Case filter_001

**Question:** Find all customers from Germany.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax FROM customers WHERE country = 'Germany'
```

**Expected SQL:**

```sql
SELECT * FROM customers WHERE country = 'Germany'
```

**Expected Rows:**

Showing first 5 of 11 rows.

```json
[
  {
    "customer_id": "ALFKI",
    "company_name": "Alfreds Futterkiste",
    "contact_name": "Maria Anders",
    "contact_title": "Sales Representative",
    "address": "Obere Str. 57",
    "city": "Berlin",
    "region": null,
    "postal_code": "12209",
    "country": "Germany",
    "phone": "030-0074321",
    "fax": "030-0076545"
  },
  {
    "customer_id": "BLAUS",
    "company_name": "Blauer See Delikatessen",
    "contact_name": "Hanna Moos",
    "contact_title": "Sales Representative",
    "address": "Forsterstr. 57",
    "city": "Mannheim",
    "region": null,
    "postal_code": "68306",
    "country": "Germany",
    "phone": "0621-08460",
    "fax": "0621-08924"
  },
  {
    "customer_id": "DRACD",
    "company_name": "Drachenblut Delikatessen",
    "contact_name": "Sven Ottlieb",
    "contact_title": "Order Administrator",
    "address": "Walserweg 21",
    "city": "Aachen",
    "region": null,
    "postal_code": "52066",
    "country": "Germany",
    "phone": "0241-039123",
    "fax": "0241-059428"
  },
  {
    "customer_id": "FRANK",
    "company_name": "Frankenversand",
    "contact_name": "Peter Franken",
    "contact_title": "Marketing Manager",
    "address": "Berliner Platz 43",
    "city": "München",
    "region": null,
    "postal_code": "80805",
    "country": "Germany",
    "phone": "089-0877310",
    "fax": "089-0877451"
  },
  {
    "customer_id": "KOENE",
    "company_name": "Königlich Essen",
    "contact_name": "Philip Cramer",
    "contact_title": "Sales Associate",
    "address": "Maubelstr. 90",
    "city": "Brandenburg",
    "region": null,
    "postal_code": "14776",
    "country": "Germany",
    "phone": "0555-09876",
    "fax": null
  }
]
```

**Generated Rows:**

Showing first 5 of 11 rows.

```json
[
  {
    "customer_id": "ALFKI",
    "company_name": "Alfreds Futterkiste",
    "contact_name": "Maria Anders",
    "contact_title": "Sales Representative",
    "address": "Obere Str. 57",
    "city": "Berlin",
    "region": null,
    "postal_code": "12209",
    "country": "Germany",
    "phone": "030-0074321",
    "fax": "030-0076545"
  },
  {
    "customer_id": "BLAUS",
    "company_name": "Blauer See Delikatessen",
    "contact_name": "Hanna Moos",
    "contact_title": "Sales Representative",
    "address": "Forsterstr. 57",
    "city": "Mannheim",
    "region": null,
    "postal_code": "68306",
    "country": "Germany",
    "phone": "0621-08460",
    "fax": "0621-08924"
  },
  {
    "customer_id": "DRACD",
    "company_name": "Drachenblut Delikatessen",
    "contact_name": "Sven Ottlieb",
    "contact_title": "Order Administrator",
    "address": "Walserweg 21",
    "city": "Aachen",
    "region": null,
    "postal_code": "52066",
    "country": "Germany",
    "phone": "0241-039123",
    "fax": "0241-059428"
  },
  {
    "customer_id": "FRANK",
    "company_name": "Frankenversand",
    "contact_name": "Peter Franken",
    "contact_title": "Marketing Manager",
    "address": "Berliner Platz 43",
    "city": "München",
    "region": null,
    "postal_code": "80805",
    "country": "Germany",
    "phone": "089-0877310",
    "fax": "089-0877451"
  },
  {
    "customer_id": "KOENE",
    "company_name": "Königlich Essen",
    "contact_name": "Philip Cramer",
    "contact_title": "Sales Associate",
    "address": "Maubelstr. 90",
    "city": "Brandenburg",
    "region": null,
    "postal_code": "14776",
    "country": "Germany",
    "phone": "0555-09876",
    "fax": null
  }
]
```

**Error:** None

### Case filter_002

**Question:** Find customers located in France.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax FROM customers WHERE country = 'France'
```

**Expected SQL:**

```sql
SELECT * FROM customers WHERE country = 'France'
```

**Expected Rows:**

Showing first 5 of 11 rows.

```json
[
  {
    "customer_id": "BLONP",
    "company_name": "Blondesddsl père et fils",
    "contact_name": "Frédérique Citeaux",
    "contact_title": "Marketing Manager",
    "address": "24, place Kléber",
    "city": "Strasbourg",
    "region": null,
    "postal_code": "67000",
    "country": "France",
    "phone": "88.60.15.31",
    "fax": "88.60.15.32"
  },
  {
    "customer_id": "BONAP",
    "company_name": "Bon app'",
    "contact_name": "Laurence Lebihan",
    "contact_title": "Owner",
    "address": "12, rue des Bouchers",
    "city": "Marseille",
    "region": null,
    "postal_code": "13008",
    "country": "France",
    "phone": "91.24.45.40",
    "fax": "91.24.45.41"
  },
  {
    "customer_id": "DUMON",
    "company_name": "Du monde entier",
    "contact_name": "Janine Labrune",
    "contact_title": "Owner",
    "address": "67, rue des Cinquante Otages",
    "city": "Nantes",
    "region": null,
    "postal_code": "44000",
    "country": "France",
    "phone": "40.67.88.88",
    "fax": "40.67.89.89"
  },
  {
    "customer_id": "FOLIG",
    "company_name": "Folies gourmandes",
    "contact_name": "Martine Rancé",
    "contact_title": "Assistant Sales Agent",
    "address": "184, chaussée de Tournai",
    "city": "Lille",
    "region": null,
    "postal_code": "59000",
    "country": "France",
    "phone": "20.16.10.16",
    "fax": "20.16.10.17"
  },
  {
    "customer_id": "FRANR",
    "company_name": "France restauration",
    "contact_name": "Carine Schmitt",
    "contact_title": "Marketing Manager",
    "address": "54, rue Royale",
    "city": "Nantes",
    "region": null,
    "postal_code": "44000",
    "country": "France",
    "phone": "40.32.21.21",
    "fax": "40.32.21.20"
  }
]
```

**Generated Rows:**

Showing first 5 of 11 rows.

```json
[
  {
    "customer_id": "BLONP",
    "company_name": "Blondesddsl père et fils",
    "contact_name": "Frédérique Citeaux",
    "contact_title": "Marketing Manager",
    "address": "24, place Kléber",
    "city": "Strasbourg",
    "region": null,
    "postal_code": "67000",
    "country": "France",
    "phone": "88.60.15.31",
    "fax": "88.60.15.32"
  },
  {
    "customer_id": "BONAP",
    "company_name": "Bon app'",
    "contact_name": "Laurence Lebihan",
    "contact_title": "Owner",
    "address": "12, rue des Bouchers",
    "city": "Marseille",
    "region": null,
    "postal_code": "13008",
    "country": "France",
    "phone": "91.24.45.40",
    "fax": "91.24.45.41"
  },
  {
    "customer_id": "DUMON",
    "company_name": "Du monde entier",
    "contact_name": "Janine Labrune",
    "contact_title": "Owner",
    "address": "67, rue des Cinquante Otages",
    "city": "Nantes",
    "region": null,
    "postal_code": "44000",
    "country": "France",
    "phone": "40.67.88.88",
    "fax": "40.67.89.89"
  },
  {
    "customer_id": "FOLIG",
    "company_name": "Folies gourmandes",
    "contact_name": "Martine Rancé",
    "contact_title": "Assistant Sales Agent",
    "address": "184, chaussée de Tournai",
    "city": "Lille",
    "region": null,
    "postal_code": "59000",
    "country": "France",
    "phone": "20.16.10.16",
    "fax": "20.16.10.17"
  },
  {
    "customer_id": "FRANR",
    "company_name": "France restauration",
    "contact_name": "Carine Schmitt",
    "contact_title": "Marketing Manager",
    "address": "54, rue Royale",
    "city": "Nantes",
    "region": null,
    "postal_code": "44000",
    "country": "France",
    "phone": "40.32.21.21",
    "fax": "40.32.21.20"
  }
]
```

**Error:** None

### Case filter_003

**Question:** List products that cost more than 50.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT product_id, product_name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued FROM products WHERE unit_price > 50
```

**Expected SQL:**

```sql
SELECT * FROM products WHERE unit_price > 50
```

**Expected Rows:**

Showing first 5 of 7 rows.

```json
[
  {
    "product_id": 9,
    "product_name": "Mishi Kobe Niku",
    "supplier_id": 4,
    "category_id": 6,
    "quantity_per_unit": "18 - 500 g pkgs.",
    "unit_price": 97.0,
    "units_in_stock": 29,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 1
  },
  {
    "product_id": 18,
    "product_name": "Carnarvon Tigers",
    "supplier_id": 7,
    "category_id": 8,
    "quantity_per_unit": "16 kg pkg.",
    "unit_price": 62.5,
    "units_in_stock": 42,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 0
  },
  {
    "product_id": 20,
    "product_name": "Sir Rodney's Marmalade",
    "supplier_id": 8,
    "category_id": 3,
    "quantity_per_unit": "30 gift boxes",
    "unit_price": 81.0,
    "units_in_stock": 40,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 0
  },
  {
    "product_id": 29,
    "product_name": "Thüringer Rostbratwurst",
    "supplier_id": 12,
    "category_id": 6,
    "quantity_per_unit": "50 bags x 30 sausgs.",
    "unit_price": 123.79,
    "units_in_stock": 0,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 1
  },
  {
    "product_id": 38,
    "product_name": "Côte de Blaye",
    "supplier_id": 18,
    "category_id": 1,
    "quantity_per_unit": "12 - 75 cl bottles",
    "unit_price": 263.5,
    "units_in_stock": 17,
    "units_on_order": 0,
    "reorder_level": 15,
    "discontinued": 0
  }
]
```

**Generated Rows:**

Showing first 5 of 7 rows.

```json
[
  {
    "product_id": 9,
    "product_name": "Mishi Kobe Niku",
    "supplier_id": 4,
    "category_id": 6,
    "quantity_per_unit": "18 - 500 g pkgs.",
    "unit_price": 97.0,
    "units_in_stock": 29,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 1
  },
  {
    "product_id": 18,
    "product_name": "Carnarvon Tigers",
    "supplier_id": 7,
    "category_id": 8,
    "quantity_per_unit": "16 kg pkg.",
    "unit_price": 62.5,
    "units_in_stock": 42,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 0
  },
  {
    "product_id": 20,
    "product_name": "Sir Rodney's Marmalade",
    "supplier_id": 8,
    "category_id": 3,
    "quantity_per_unit": "30 gift boxes",
    "unit_price": 81.0,
    "units_in_stock": 40,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 0
  },
  {
    "product_id": 29,
    "product_name": "Thüringer Rostbratwurst",
    "supplier_id": 12,
    "category_id": 6,
    "quantity_per_unit": "50 bags x 30 sausgs.",
    "unit_price": 123.79,
    "units_in_stock": 0,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 1
  },
  {
    "product_id": 38,
    "product_name": "Côte de Blaye",
    "supplier_id": 18,
    "category_id": 1,
    "quantity_per_unit": "12 - 75 cl bottles",
    "unit_price": 263.5,
    "units_in_stock": 17,
    "units_on_order": 0,
    "reorder_level": 15,
    "discontinued": 0
  }
]
```

**Error:** None

### Case filter_005

**Question:** Find all employees hired after 1993.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT employee_id, last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes, reports_to, photo_path FROM employees WHERE hire_date > '1993-01-01'
```

**Expected SQL:**

```sql
SELECT * FROM employees WHERE hire_date > '1993-01-01'
```

**Expected Rows:**

Showing first 5 of 6 rows.

```json
[
  {
    "employee_id": 4,
    "last_name": "Peacock",
    "first_name": "Margaret",
    "title": "Sales Representative",
    "title_of_courtesy": "Mrs.",
    "birth_date": "1937-09-19",
    "hire_date": "1993-05-03",
    "address": "4110 Old Redmond Rd.",
    "city": "Redmond",
    "region": "WA",
    "postal_code": "98052",
    "country": "USA",
    "home_phone": "(206) 555-8122",
    "extension": "5176",
    "photo": "",
    "notes": "Margaret holds a BA in English literature from Concordia College (1958) and an MA from the American Institute of Culinary Arts (1966).  She was assigned to the London office temporarily from July through November 1992.",
    "reports_to": 2,
    "photo_path": "http://accweb/emmployees/peacock.bmp"
  },
  {
    "employee_id": 5,
    "last_name": "Buchanan",
    "first_name": "Steven",
    "title": "Sales Manager",
    "title_of_courtesy": "Mr.",
    "birth_date": "1955-03-04",
    "hire_date": "1993-10-17",
    "address": "14 Garrett Hill",
    "city": "London",
    "region": null,
    "postal_code": "SW1 8JR",
    "country": "UK",
    "home_phone": "(71) 555-4848",
    "extension": "3453",
    "photo": "",
    "notes": "Steven Buchanan graduated from St. Andrews University, Scotland, with a BSC degree in 1976.  Upon joining the company as a sales representative in 1992, he spent 6 months in an orientation program at the Seattle office and then returned to his permanent post in London.  He was promoted to sales manager in March 1993.  Mr. Buchanan has completed the courses Successful Telemarketing and International Sales Management.  He is fluent in French.",
    "reports_to": 2,
    "photo_path": "http://accweb/emmployees/buchanan.bmp"
  },
  {
    "employee_id": 6,
    "last_name": "Suyama",
    "first_name": "Michael",
    "title": "Sales Representative",
    "title_of_courtesy": "Mr.",
    "birth_date": "1963-07-02",
    "hire_date": "1993-10-17",
    "address": "Coventry House\\nMiner Rd.",
    "city": "London",
    "region": null,
    "postal_code": "EC2 7JR",
    "country": "UK",
    "home_phone": "(71) 555-7773",
    "extension": "428",
    "photo": "",
    "notes": "Michael is a graduate of Sussex University (MA, economics, 1983) and the University of California at Los Angeles (MBA, marketing, 1986).  He has also taken the courses Multi-Cultural Selling and Time Management for the Sales Professional.  He is fluent in Japanese and can read and write French, Portuguese, and Spanish.",
    "reports_to": 5,
    "photo_path": "http://accweb/emmployees/davolio.bmp"
  },
  {
    "employee_id": 7,
    "last_name": "King",
    "first_name": "Robert",
    "title": "Sales Representative",
    "title_of_courtesy": "Mr.",
    "birth_date": "1960-05-29",
    "hire_date": "1994-01-02",
    "address": "Edgeham Hollow\\nWinchester Way",
    "city": "London",
    "region": null,
    "postal_code": "RG1 9SP",
    "country": "UK",
    "home_phone": "(71) 555-5598",
    "extension": "465",
    "photo": "",
    "notes": "Robert King served in the Peace Corps and traveled extensively before completing his degree in English at the University of Michigan in 1992, the year he joined the company.  After completing a course entitled Selling in Europe, he was transferred to the London office in March 1993.",
    "reports_to": 5,
    "photo_path": "http://accweb/emmployees/davolio.bmp"
  },
  {
    "employee_id": 8,
    "last_name": "Callahan",
    "first_name": "Laura",
    "title": "Inside Sales Coordinator",
    "title_of_courtesy": "Ms.",
    "birth_date": "1958-01-09",
    "hire_date": "1994-03-05",
    "address": "4726 - 11th Ave. N.E.",
    "city": "Seattle",
    "region": "WA",
    "postal_code": "98105",
    "country": "USA",
    "home_phone": "(206) 555-1189",
    "extension": "2344",
    "photo": "",
    "notes": "Laura received a BA in psychology from the University of Washington.  She has also completed a course in business French.  She reads and writes French.",
    "reports_to": 2,
    "photo_path": "http://accweb/emmployees/davolio.bmp"
  }
]
```

**Generated Rows:**

Showing first 5 of 6 rows.

```json
[
  {
    "employee_id": 4,
    "last_name": "Peacock",
    "first_name": "Margaret",
    "title": "Sales Representative",
    "title_of_courtesy": "Mrs.",
    "birth_date": "1937-09-19",
    "hire_date": "1993-05-03",
    "address": "4110 Old Redmond Rd.",
    "city": "Redmond",
    "region": "WA",
    "postal_code": "98052",
    "country": "USA",
    "home_phone": "(206) 555-8122",
    "extension": "5176",
    "photo": "",
    "notes": "Margaret holds a BA in English literature from Concordia College (1958) and an MA from the American Institute of Culinary Arts (1966).  She was assigned to the London office temporarily from July through November 1992.",
    "reports_to": 2,
    "photo_path": "http://accweb/emmployees/peacock.bmp"
  },
  {
    "employee_id": 5,
    "last_name": "Buchanan",
    "first_name": "Steven",
    "title": "Sales Manager",
    "title_of_courtesy": "Mr.",
    "birth_date": "1955-03-04",
    "hire_date": "1993-10-17",
    "address": "14 Garrett Hill",
    "city": "London",
    "region": null,
    "postal_code": "SW1 8JR",
    "country": "UK",
    "home_phone": "(71) 555-4848",
    "extension": "3453",
    "photo": "",
    "notes": "Steven Buchanan graduated from St. Andrews University, Scotland, with a BSC degree in 1976.  Upon joining the company as a sales representative in 1992, he spent 6 months in an orientation program at the Seattle office and then returned to his permanent post in London.  He was promoted to sales manager in March 1993.  Mr. Buchanan has completed the courses Successful Telemarketing and International Sales Management.  He is fluent in French.",
    "reports_to": 2,
    "photo_path": "http://accweb/emmployees/buchanan.bmp"
  },
  {
    "employee_id": 6,
    "last_name": "Suyama",
    "first_name": "Michael",
    "title": "Sales Representative",
    "title_of_courtesy": "Mr.",
    "birth_date": "1963-07-02",
    "hire_date": "1993-10-17",
    "address": "Coventry House\\nMiner Rd.",
    "city": "London",
    "region": null,
    "postal_code": "EC2 7JR",
    "country": "UK",
    "home_phone": "(71) 555-7773",
    "extension": "428",
    "photo": "",
    "notes": "Michael is a graduate of Sussex University (MA, economics, 1983) and the University of California at Los Angeles (MBA, marketing, 1986).  He has also taken the courses Multi-Cultural Selling and Time Management for the Sales Professional.  He is fluent in Japanese and can read and write French, Portuguese, and Spanish.",
    "reports_to": 5,
    "photo_path": "http://accweb/emmployees/davolio.bmp"
  },
  {
    "employee_id": 7,
    "last_name": "King",
    "first_name": "Robert",
    "title": "Sales Representative",
    "title_of_courtesy": "Mr.",
    "birth_date": "1960-05-29",
    "hire_date": "1994-01-02",
    "address": "Edgeham Hollow\\nWinchester Way",
    "city": "London",
    "region": null,
    "postal_code": "RG1 9SP",
    "country": "UK",
    "home_phone": "(71) 555-5598",
    "extension": "465",
    "photo": "",
    "notes": "Robert King served in the Peace Corps and traveled extensively before completing his degree in English at the University of Michigan in 1992, the year he joined the company.  After completing a course entitled Selling in Europe, he was transferred to the London office in March 1993.",
    "reports_to": 5,
    "photo_path": "http://accweb/emmployees/davolio.bmp"
  },
  {
    "employee_id": 8,
    "last_name": "Callahan",
    "first_name": "Laura",
    "title": "Inside Sales Coordinator",
    "title_of_courtesy": "Ms.",
    "birth_date": "1958-01-09",
    "hire_date": "1994-03-05",
    "address": "4726 - 11th Ave. N.E.",
    "city": "Seattle",
    "region": "WA",
    "postal_code": "98105",
    "country": "USA",
    "home_phone": "(206) 555-1189",
    "extension": "2344",
    "photo": "",
    "notes": "Laura received a BA in psychology from the University of Washington.  She has also completed a course in business French.  She reads and writes French.",
    "reports_to": 2,
    "photo_path": "http://accweb/emmployees/davolio.bmp"
  }
]
```

**Error:** None

### Case filter_008

**Question:** List products with stock below 20 units.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT product_id, product_name, units_in_stock FROM products WHERE units_in_stock < 20
```

**Expected SQL:**

```sql
SELECT * FROM products WHERE units_in_stock < 20
```

**Expected Rows:**

Showing first 5 of 26 rows.

```json
[
  {
    "product_id": 2,
    "product_name": "Chang",
    "supplier_id": 1,
    "category_id": 1,
    "quantity_per_unit": "24 - 12 oz bottles",
    "unit_price": 19.0,
    "units_in_stock": 17,
    "units_on_order": 40,
    "reorder_level": 25,
    "discontinued": 1
  },
  {
    "product_id": 3,
    "product_name": "Aniseed Syrup",
    "supplier_id": 1,
    "category_id": 2,
    "quantity_per_unit": "12 - 550 ml bottles",
    "unit_price": 10.0,
    "units_in_stock": 13,
    "units_on_order": 70,
    "reorder_level": 25,
    "discontinued": 0
  },
  {
    "product_id": 5,
    "product_name": "Chef Anton's Gumbo Mix",
    "supplier_id": 2,
    "category_id": 2,
    "quantity_per_unit": "36 boxes",
    "unit_price": 21.35,
    "units_in_stock": 0,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 1
  },
  {
    "product_id": 7,
    "product_name": "Uncle Bob's Organic Dried Pears",
    "supplier_id": 3,
    "category_id": 7,
    "quantity_per_unit": "12 - 1 lb pkgs.",
    "unit_price": 30.0,
    "units_in_stock": 15,
    "units_on_order": 0,
    "reorder_level": 10,
    "discontinued": 0
  },
  {
    "product_id": 8,
    "product_name": "Northwoods Cranberry Sauce",
    "supplier_id": 3,
    "category_id": 2,
    "quantity_per_unit": "12 - 12 oz jars",
    "unit_price": 40.0,
    "units_in_stock": 6,
    "units_on_order": 0,
    "reorder_level": 0,
    "discontinued": 0
  }
]
```

**Generated Rows:**

Showing first 5 of 26 rows.

```json
[
  {
    "product_id": 2,
    "product_name": "Chang",
    "units_in_stock": 17
  },
  {
    "product_id": 3,
    "product_name": "Aniseed Syrup",
    "units_in_stock": 13
  },
  {
    "product_id": 5,
    "product_name": "Chef Anton's Gumbo Mix",
    "units_in_stock": 0
  },
  {
    "product_id": 7,
    "product_name": "Uncle Bob's Organic Dried Pears",
    "units_in_stock": 15
  },
  {
    "product_id": 8,
    "product_name": "Northwoods Cranberry Sauce",
    "units_in_stock": 6
  }
]
```

**Error:** None

### Case filter_009

**Question:** Find orders shipped to France or Germany.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT * FROM orders WHERE ship_country IN ('France', 'Germany')
```

**Expected SQL:**

```sql
SELECT * FROM orders WHERE ship_country IN ('France','Germany')
```

**Expected Rows:**

Showing first 5 of 199 rows.

```json
[
  {
    "order_id": 10248,
    "customer_id": "VINET",
    "employee_id": 5,
    "order_date": "1996-07-04",
    "required_date": "1996-08-01",
    "shipped_date": "1996-07-16",
    "ship_via": 3,
    "freight": 32.38,
    "ship_name": "Vins et alcools Chevalier",
    "ship_address": "59 rue de l'Abbaye",
    "ship_city": "Reims",
    "ship_region": null,
    "ship_postal_code": "51100",
    "ship_country": "France"
  },
  {
    "order_id": 10249,
    "customer_id": "TOMSP",
    "employee_id": 6,
    "order_date": "1996-07-05",
    "required_date": "1996-08-16",
    "shipped_date": "1996-07-10",
    "ship_via": 1,
    "freight": 11.61,
    "ship_name": "Toms Spezialitäten",
    "ship_address": "Luisenstr. 48",
    "ship_city": "Münster",
    "ship_region": null,
    "ship_postal_code": "44087",
    "ship_country": "Germany"
  },
  {
    "order_id": 10251,
    "customer_id": "VICTE",
    "employee_id": 3,
    "order_date": "1996-07-08",
    "required_date": "1996-08-05",
    "shipped_date": "1996-07-15",
    "ship_via": 1,
    "freight": 41.34,
    "ship_name": "Victuailles en stock",
    "ship_address": "2, rue du Commerce",
    "ship_city": "Lyon",
    "ship_region": null,
    "ship_postal_code": "69004",
    "ship_country": "France"
  },
  {
    "order_id": 10260,
    "customer_id": "OTTIK",
    "employee_id": 4,
    "order_date": "1996-07-19",
    "required_date": "1996-08-16",
    "shipped_date": "1996-07-29",
    "ship_via": 1,
    "freight": 55.09,
    "ship_name": "Ottilies Käseladen",
    "ship_address": "Mehrheimerstr. 369",
    "ship_city": "Köln",
    "ship_region": null,
    "ship_postal_code": "50739",
    "ship_country": "Germany"
  },
  {
    "order_id": 10265,
    "customer_id": "BLONP",
    "employee_id": 2,
    "order_date": "1996-07-25",
    "required_date": "1996-08-22",
    "shipped_date": "1996-08-12",
    "ship_via": 1,
    "freight": 55.28,
    "ship_name": "Blondel père et fils",
    "ship_address": "24, place Kléber",
    "ship_city": "Strasbourg",
    "ship_region": null,
    "ship_postal_code": "67000",
    "ship_country": "France"
  }
]
```

**Generated Rows:**

Showing first 5 of 199 rows.

```json
[
  {
    "order_id": 10248,
    "customer_id": "VINET",
    "employee_id": 5,
    "order_date": "1996-07-04",
    "required_date": "1996-08-01",
    "shipped_date": "1996-07-16",
    "ship_via": 3,
    "freight": 32.38,
    "ship_name": "Vins et alcools Chevalier",
    "ship_address": "59 rue de l'Abbaye",
    "ship_city": "Reims",
    "ship_region": null,
    "ship_postal_code": "51100",
    "ship_country": "France"
  },
  {
    "order_id": 10249,
    "customer_id": "TOMSP",
    "employee_id": 6,
    "order_date": "1996-07-05",
    "required_date": "1996-08-16",
    "shipped_date": "1996-07-10",
    "ship_via": 1,
    "freight": 11.61,
    "ship_name": "Toms Spezialitäten",
    "ship_address": "Luisenstr. 48",
    "ship_city": "Münster",
    "ship_region": null,
    "ship_postal_code": "44087",
    "ship_country": "Germany"
  },
  {
    "order_id": 10251,
    "customer_id": "VICTE",
    "employee_id": 3,
    "order_date": "1996-07-08",
    "required_date": "1996-08-05",
    "shipped_date": "1996-07-15",
    "ship_via": 1,
    "freight": 41.34,
    "ship_name": "Victuailles en stock",
    "ship_address": "2, rue du Commerce",
    "ship_city": "Lyon",
    "ship_region": null,
    "ship_postal_code": "69004",
    "ship_country": "France"
  },
  {
    "order_id": 10260,
    "customer_id": "OTTIK",
    "employee_id": 4,
    "order_date": "1996-07-19",
    "required_date": "1996-08-16",
    "shipped_date": "1996-07-29",
    "ship_via": 1,
    "freight": 55.09,
    "ship_name": "Ottilies Käseladen",
    "ship_address": "Mehrheimerstr. 369",
    "ship_city": "Köln",
    "ship_region": null,
    "ship_postal_code": "50739",
    "ship_country": "Germany"
  },
  {
    "order_id": 10265,
    "customer_id": "BLONP",
    "employee_id": 2,
    "order_date": "1996-07-25",
    "required_date": "1996-08-22",
    "shipped_date": "1996-08-12",
    "ship_via": 1,
    "freight": 55.28,
    "ship_name": "Blondel père et fils",
    "ship_address": "24, place Kléber",
    "ship_city": "Strasbourg",
    "ship_region": null,
    "ship_postal_code": "67000",
    "ship_country": "France"
  }
]
```

**Error:** None

### Case filter_010

**Question:** Find customers without a fax number.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax FROM customers WHERE fax IS NULL
```

**Expected SQL:**

```sql
SELECT * FROM customers WHERE fax IS NULL
```

**Expected Rows:**

Showing first 5 of 22 rows.

```json
[
  {
    "customer_id": "ANTON",
    "company_name": "Antonio Moreno Taquería",
    "contact_name": "Antonio Moreno",
    "contact_title": "Owner",
    "address": "Mataderos  2312",
    "city": "México D.F.",
    "region": null,
    "postal_code": "05023",
    "country": "Mexico",
    "phone": "(5) 555-3932",
    "fax": null
  },
  {
    "customer_id": "BSBEV",
    "company_name": "B's Beverages",
    "contact_name": "Victoria Ashworth",
    "contact_title": "Sales Representative",
    "address": "Fauntleroy Circus",
    "city": "London",
    "region": null,
    "postal_code": "EC2 5NT",
    "country": "UK",
    "phone": "(171) 555-1212",
    "fax": null
  },
  {
    "customer_id": "CHOPS",
    "company_name": "Chop-suey Chinese",
    "contact_name": "Yang Wang",
    "contact_title": "Owner",
    "address": "Hauptstr. 29",
    "city": "Bern",
    "region": null,
    "postal_code": "3012",
    "country": "Switzerland",
    "phone": "0452-076545",
    "fax": null
  },
  {
    "customer_id": "COMMI",
    "company_name": "Comércio Mineiro",
    "contact_name": "Pedro Afonso",
    "contact_title": "Sales Associate",
    "address": "Av. dos Lusíadas, 23",
    "city": "Sao Paulo",
    "region": "SP",
    "postal_code": "05432-043",
    "country": "Brazil",
    "phone": "(11) 555-7647",
    "fax": null
  },
  {
    "customer_id": "FAMIA",
    "company_name": "Familia Arquibaldo",
    "contact_name": "Aria Cruz",
    "contact_title": "Marketing Assistant",
    "address": "Rua Orós, 92",
    "city": "Sao Paulo",
    "region": "SP",
    "postal_code": "05442-030",
    "country": "Brazil",
    "phone": "(11) 555-9857",
    "fax": null
  }
]
```

**Generated Rows:**

Showing first 5 of 22 rows.

```json
[
  {
    "customer_id": "ANTON",
    "company_name": "Antonio Moreno Taquería",
    "contact_name": "Antonio Moreno",
    "contact_title": "Owner",
    "address": "Mataderos  2312",
    "city": "México D.F.",
    "region": null,
    "postal_code": "05023",
    "country": "Mexico",
    "phone": "(5) 555-3932",
    "fax": null
  },
  {
    "customer_id": "BSBEV",
    "company_name": "B's Beverages",
    "contact_name": "Victoria Ashworth",
    "contact_title": "Sales Representative",
    "address": "Fauntleroy Circus",
    "city": "London",
    "region": null,
    "postal_code": "EC2 5NT",
    "country": "UK",
    "phone": "(171) 555-1212",
    "fax": null
  },
  {
    "customer_id": "CHOPS",
    "company_name": "Chop-suey Chinese",
    "contact_name": "Yang Wang",
    "contact_title": "Owner",
    "address": "Hauptstr. 29",
    "city": "Bern",
    "region": null,
    "postal_code": "3012",
    "country": "Switzerland",
    "phone": "0452-076545",
    "fax": null
  },
  {
    "customer_id": "COMMI",
    "company_name": "Comércio Mineiro",
    "contact_name": "Pedro Afonso",
    "contact_title": "Sales Associate",
    "address": "Av. dos Lusíadas, 23",
    "city": "Sao Paulo",
    "region": "SP",
    "postal_code": "05432-043",
    "country": "Brazil",
    "phone": "(11) 555-7647",
    "fax": null
  },
  {
    "customer_id": "FAMIA",
    "company_name": "Familia Arquibaldo",
    "contact_name": "Aria Cruz",
    "contact_title": "Marketing Assistant",
    "address": "Rua Orós, 92",
    "city": "Sao Paulo",
    "region": "SP",
    "postal_code": "05442-030",
    "country": "Brazil",
    "phone": "(11) 555-9857",
    "fax": null
  }
]
```

**Error:** None

### Case join_001

**Question:** Which customers have placed orders?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT DISTINCT c.* FROM customers c JOIN orders o ON c.customer_id = o.customer_id
```

**Expected SQL:**

```sql
SELECT DISTINCT customers.company_name FROM customers JOIN orders ON customers.customer_id = orders.customer_id
```

**Expected Rows:**

Showing first 5 of 89 rows.

```json
[
  {
    "company_name": "Wilman Kala"
  },
  {
    "company_name": "Magazzini Alimentari Riuniti"
  },
  {
    "company_name": "The Cracker Box"
  },
  {
    "company_name": "Wellington Importadora"
  },
  {
    "company_name": "Let's Stop N Shop"
  }
]
```

**Generated Rows:**

Showing first 5 of 89 rows.

```json
[
  {
    "customer_id": "REGGC",
    "company_name": "Reggiani Caseifici",
    "contact_name": "Maurizio Moroni",
    "contact_title": "Sales Associate",
    "address": "Strada Provinciale 124",
    "city": "Reggio Emilia",
    "region": null,
    "postal_code": "42100",
    "country": "Italy",
    "phone": "0522-556721",
    "fax": "0522-556722"
  },
  {
    "customer_id": "HILAA",
    "company_name": "HILARION-Abastos",
    "contact_name": "Carlos Hernández",
    "contact_title": "Sales Representative",
    "address": "Carrera 22 con Ave. Carlos Soublette #8-35",
    "city": "San Cristóbal",
    "region": "Táchira",
    "postal_code": "5022",
    "country": "Venezuela",
    "phone": "(5) 555-1340",
    "fax": "(5) 555-1948"
  },
  {
    "customer_id": "BSBEV",
    "company_name": "B's Beverages",
    "contact_name": "Victoria Ashworth",
    "contact_title": "Sales Representative",
    "address": "Fauntleroy Circus",
    "city": "London",
    "region": null,
    "postal_code": "EC2 5NT",
    "country": "UK",
    "phone": "(171) 555-1212",
    "fax": null
  },
  {
    "customer_id": "BERGS",
    "company_name": "Berglunds snabbköp",
    "contact_name": "Christina Berglund",
    "contact_title": "Order Administrator",
    "address": "Berguvsvägen  8",
    "city": "Luleå",
    "region": null,
    "postal_code": "S-958 22",
    "country": "Sweden",
    "phone": "0921-12 34 65",
    "fax": "0921-12 34 67"
  },
  {
    "customer_id": "WANDK",
    "company_name": "Die Wandernde Kuh",
    "contact_name": "Rita Müller",
    "contact_title": "Sales Representative",
    "address": "Adenauerallee 900",
    "city": "Stuttgart",
    "region": null,
    "postal_code": "70563",
    "country": "Germany",
    "phone": "0711-020361",
    "fax": "0711-035428"
  }
]
```

**Error:** None

### Case join_002

**Question:** How many orders has each customer placed?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT c.customer_id, COUNT(o.order_id) AS order_count FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id
```

**Expected SQL:**

```sql
SELECT customers.company_name, COUNT(orders.order_id) FROM customers JOIN orders ON customers.customer_id = orders.customer_id GROUP BY customers.company_name
```

**Expected Rows:**

Showing first 5 of 89 rows.

```json
[
  {
    "company_name": "Wilman Kala",
    "count": 7
  },
  {
    "company_name": "Magazzini Alimentari Riuniti",
    "count": 10
  },
  {
    "company_name": "The Cracker Box",
    "count": 3
  },
  {
    "company_name": "Wellington Importadora",
    "count": 9
  },
  {
    "company_name": "Let's Stop N Shop",
    "count": 4
  }
]
```

**Generated Rows:**

Showing first 5 of 89 rows.

```json
[
  {
    "customer_id": "TOMSP",
    "order_count": 6
  },
  {
    "customer_id": "LONEP",
    "order_count": 8
  },
  {
    "customer_id": "OLDWO",
    "order_count": 10
  },
  {
    "customer_id": "WARTH",
    "order_count": 15
  },
  {
    "customer_id": "MAGAA",
    "order_count": 10
  }
]
```

**Error:** None

### Case join_003

**Question:** List all products with their category names.

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT products.product_name, categories.category_name FROM products INNER JOIN categories ON products.category_id = categories.category_id
```

**Expected SQL:**

```sql
SELECT products.product_name, categories.category_name FROM products JOIN categories ON products.category_id = categories.category_id
```

**Expected Rows:**

Showing first 5 of 77 rows.

```json
[
  {
    "product_name": "Chai",
    "category_name": "Beverages"
  },
  {
    "product_name": "Chang",
    "category_name": "Beverages"
  },
  {
    "product_name": "Aniseed Syrup",
    "category_name": "Condiments"
  },
  {
    "product_name": "Chef Anton's Cajun Seasoning",
    "category_name": "Condiments"
  },
  {
    "product_name": "Chef Anton's Gumbo Mix",
    "category_name": "Condiments"
  }
]
```

**Generated Rows:**

Showing first 5 of 77 rows.

```json
[
  {
    "product_name": "Chai",
    "category_name": "Beverages"
  },
  {
    "product_name": "Chang",
    "category_name": "Beverages"
  },
  {
    "product_name": "Aniseed Syrup",
    "category_name": "Condiments"
  },
  {
    "product_name": "Chef Anton's Cajun Seasoning",
    "category_name": "Condiments"
  },
  {
    "product_name": "Chef Anton's Gumbo Mix",
    "category_name": "Condiments"
  }
]
```

**Error:** None

### Case join_004

**Question:** Show each order with the customer's company name.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT orders.*, customers.company_name AS customer_company_name FROM orders JOIN customers ON orders.customer_id = customers.customer_id
```

**Expected SQL:**

```sql
SELECT orders.order_id, customers.company_name FROM orders JOIN customers ON orders.customer_id = customers.customer_id
```

**Expected Rows:**

Showing first 5 of 830 rows.

```json
[
  {
    "order_id": 10248,
    "company_name": "Vins et alcools Chevalier"
  },
  {
    "order_id": 10249,
    "company_name": "Toms Spezialitäten"
  },
  {
    "order_id": 10250,
    "company_name": "Hanari Carnes"
  },
  {
    "order_id": 10251,
    "company_name": "Victuailles en stock"
  },
  {
    "order_id": 10252,
    "company_name": "Suprêmes délices"
  }
]
```

**Generated Rows:**

Showing first 5 of 830 rows.

```json
[
  {
    "order_id": 10248,
    "customer_id": "VINET",
    "employee_id": 5,
    "order_date": "1996-07-04",
    "required_date": "1996-08-01",
    "shipped_date": "1996-07-16",
    "ship_via": 3,
    "freight": 32.38,
    "ship_name": "Vins et alcools Chevalier",
    "ship_address": "59 rue de l'Abbaye",
    "ship_city": "Reims",
    "ship_region": null,
    "ship_postal_code": "51100",
    "ship_country": "France",
    "customer_company_name": "Vins et alcools Chevalier"
  },
  {
    "order_id": 10249,
    "customer_id": "TOMSP",
    "employee_id": 6,
    "order_date": "1996-07-05",
    "required_date": "1996-08-16",
    "shipped_date": "1996-07-10",
    "ship_via": 1,
    "freight": 11.61,
    "ship_name": "Toms Spezialitäten",
    "ship_address": "Luisenstr. 48",
    "ship_city": "Münster",
    "ship_region": null,
    "ship_postal_code": "44087",
    "ship_country": "Germany",
    "customer_company_name": "Toms Spezialitäten"
  },
  {
    "order_id": 10250,
    "customer_id": "HANAR",
    "employee_id": 4,
    "order_date": "1996-07-08",
    "required_date": "1996-08-05",
    "shipped_date": "1996-07-12",
    "ship_via": 2,
    "freight": 65.83,
    "ship_name": "Hanari Carnes",
    "ship_address": "Rua do Paço, 67",
    "ship_city": "Rio de Janeiro",
    "ship_region": "RJ",
    "ship_postal_code": "05454-876",
    "ship_country": "Brazil",
    "customer_company_name": "Hanari Carnes"
  },
  {
    "order_id": 10251,
    "customer_id": "VICTE",
    "employee_id": 3,
    "order_date": "1996-07-08",
    "required_date": "1996-08-05",
    "shipped_date": "1996-07-15",
    "ship_via": 1,
    "freight": 41.34,
    "ship_name": "Victuailles en stock",
    "ship_address": "2, rue du Commerce",
    "ship_city": "Lyon",
    "ship_region": null,
    "ship_postal_code": "69004",
    "ship_country": "France",
    "customer_company_name": "Victuailles en stock"
  },
  {
    "order_id": 10252,
    "customer_id": "SUPRD",
    "employee_id": 4,
    "order_date": "1996-07-09",
    "required_date": "1996-08-06",
    "shipped_date": "1996-07-11",
    "ship_via": 2,
    "freight": 51.3,
    "ship_name": "Suprêmes délices",
    "ship_address": "Boulevard Tirou, 255",
    "ship_city": "Charleroi",
    "ship_region": null,
    "ship_postal_code": "B-6000",
    "ship_country": "Belgium",
    "customer_company_name": "Suprêmes délices"
  }
]
```

**Error:** None

### Case join_005

**Question:** Which employees handled the most orders?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT e.employee_id, e.last_name, e.first_name, COUNT(o.order_id) AS order_count FROM employees e JOIN orders o ON e.employee_id = o.employee_id GROUP BY e.employee_id, e.last_name, e.first_name ORDER BY order_count DESC
```

**Expected SQL:**

```sql
SELECT employees.first_name, employees.last_name, COUNT(orders.order_id) FROM employees JOIN orders ON employees.employee_id = orders.employee_id GROUP BY employees.employee_id
```

**Expected Rows:**

Showing first 5 of 9 rows.

```json
[
  {
    "first_name": "Laura",
    "last_name": "Callahan",
    "count": 104
  },
  {
    "first_name": "Robert",
    "last_name": "King",
    "count": 72
  },
  {
    "first_name": "Anne",
    "last_name": "Dodsworth",
    "count": 43
  },
  {
    "first_name": "Nancy",
    "last_name": "Davolio",
    "count": 123
  },
  {
    "first_name": "Steven",
    "last_name": "Buchanan",
    "count": 42
  }
]
```

**Generated Rows:**

Showing first 5 of 9 rows.

```json
[
  {
    "employee_id": 4,
    "last_name": "Peacock",
    "first_name": "Margaret",
    "order_count": 156
  },
  {
    "employee_id": 3,
    "last_name": "Leverling",
    "first_name": "Janet",
    "order_count": 127
  },
  {
    "employee_id": 1,
    "last_name": "Davolio",
    "first_name": "Nancy",
    "order_count": 123
  },
  {
    "employee_id": 8,
    "last_name": "Callahan",
    "first_name": "Laura",
    "order_count": 104
  },
  {
    "employee_id": 2,
    "last_name": "Fuller",
    "first_name": "Andrew",
    "order_count": 96
  }
]
```

**Error:** None

### Case join_006

**Question:** Find the total sales for each product.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT p.product_id, p.product_name, SUM(od.unit_price * od.quantity * (1 - od.discount)) AS total_sales FROM order_details od JOIN products p ON od.product_id = p.product_id GROUP BY p.product_id, p.product_name
```

**Expected SQL:**

```sql
SELECT products.product_name, SUM(order_details.unit_price * order_details.quantity) FROM products JOIN order_details ON products.product_id = order_details.product_id GROUP BY products.product_name
```

**Expected Rows:**

Showing first 5 of 77 rows.

```json
[
  {
    "product_name": "Pâté chinois",
    "sum": 19512.000343322754
  },
  {
    "product_name": "Flotemysost",
    "sum": 20876.500328063965
  },
  {
    "product_name": "Camembert Pierrot",
    "sum": 50286.00037384033
  },
  {
    "product_name": "Inlagd Sill",
    "sum": 14542.599962234497
  },
  {
    "product_name": "Thüringer Rostbratwurst",
    "sum": 87736.40051269531
  }
]
```

**Generated Rows:**

Showing first 5 of 77 rows.

```json
[
  {
    "product_id": 74,
    "product_name": "Longlife Tofu",
    "total_sales": 2432.4999990463257
  },
  {
    "product_id": 54,
    "product_name": "Tourtière",
    "total_sales": 4728.237450592593
  },
  {
    "product_id": 29,
    "product_name": "Thüringer Rostbratwurst",
    "total_sales": 80368.6724385033
  },
  {
    "product_id": 71,
    "product_name": "Flotemysost",
    "total_sales": 19551.025301235914
  },
  {
    "product_id": 4,
    "product_name": "Chef Anton's Cajun Seasoning",
    "total_sales": 8567.900032654405
  }
]
```

**Error:** None

### Case join_007

**Question:** Which suppliers provide each product?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT p.product_name AS product_name, s.company_name AS supplier_company FROM products p JOIN suppliers s ON p.supplier_id = s.supplier_id
```

**Expected SQL:**

```sql
SELECT products.product_name, suppliers.company_name FROM products JOIN suppliers ON products.supplier_id = suppliers.supplier_id
```

**Expected Rows:**

Showing first 5 of 77 rows.

```json
[
  {
    "product_name": "Chai",
    "company_name": "Specialty Biscuits, Ltd."
  },
  {
    "product_name": "Chang",
    "company_name": "Exotic Liquids"
  },
  {
    "product_name": "Aniseed Syrup",
    "company_name": "Exotic Liquids"
  },
  {
    "product_name": "Chef Anton's Cajun Seasoning",
    "company_name": "New Orleans Cajun Delights"
  },
  {
    "product_name": "Chef Anton's Gumbo Mix",
    "company_name": "New Orleans Cajun Delights"
  }
]
```

**Generated Rows:**

Showing first 5 of 77 rows.

```json
[
  {
    "product_name": "Chai",
    "supplier_company": "Specialty Biscuits, Ltd."
  },
  {
    "product_name": "Chang",
    "supplier_company": "Exotic Liquids"
  },
  {
    "product_name": "Aniseed Syrup",
    "supplier_company": "Exotic Liquids"
  },
  {
    "product_name": "Chef Anton's Cajun Seasoning",
    "supplier_company": "New Orleans Cajun Delights"
  },
  {
    "product_name": "Chef Anton's Gumbo Mix",
    "supplier_company": "New Orleans Cajun Delights"
  }
]
```

**Error:** None

### Case join_008

**Question:** Find customers who bought products from the beverage category.

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT DISTINCT c.customer_id, c.company_name, c.contact_name, c.contact_title, c.address, c.city, c.region, c.postal_code, c.country, c.phone, c.fax FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_details od ON o.order_id = od.order_id JOIN products p ON od.product_id = p.product_id JOIN categories cat ON p.category_id = cat.category_id WHERE cat.category_name = 'Beverages'
```

**Expected SQL:**

```sql
SELECT DISTINCT customers.company_name FROM customers JOIN orders ON customers.customer_id = orders.customer_id JOIN order_details ON orders.order_id = order_details.order_id JOIN products ON order_details.product_id = products.product_id JOIN categories ON products.category_id = categories.category_id WHERE categories.category_name = 'Beverages'
```

**Expected Rows:**

Showing first 5 of 83 rows.

```json
[
  {
    "company_name": "Wilman Kala"
  },
  {
    "company_name": "Magazzini Alimentari Riuniti"
  },
  {
    "company_name": "The Cracker Box"
  },
  {
    "company_name": "Wellington Importadora"
  },
  {
    "company_name": "Let's Stop N Shop"
  }
]
```

**Generated Rows:**

Showing first 5 of 83 rows.

```json
[
  {
    "customer_id": "REGGC",
    "company_name": "Reggiani Caseifici",
    "contact_name": "Maurizio Moroni",
    "contact_title": "Sales Associate",
    "address": "Strada Provinciale 124",
    "city": "Reggio Emilia",
    "region": null,
    "postal_code": "42100",
    "country": "Italy",
    "phone": "0522-556721",
    "fax": "0522-556722"
  },
  {
    "customer_id": "HILAA",
    "company_name": "HILARION-Abastos",
    "contact_name": "Carlos Hernández",
    "contact_title": "Sales Representative",
    "address": "Carrera 22 con Ave. Carlos Soublette #8-35",
    "city": "San Cristóbal",
    "region": "Táchira",
    "postal_code": "5022",
    "country": "Venezuela",
    "phone": "(5) 555-1340",
    "fax": "(5) 555-1948"
  },
  {
    "customer_id": "BSBEV",
    "company_name": "B's Beverages",
    "contact_name": "Victoria Ashworth",
    "contact_title": "Sales Representative",
    "address": "Fauntleroy Circus",
    "city": "London",
    "region": null,
    "postal_code": "EC2 5NT",
    "country": "UK",
    "phone": "(171) 555-1212",
    "fax": null
  },
  {
    "customer_id": "BERGS",
    "company_name": "Berglunds snabbköp",
    "contact_name": "Christina Berglund",
    "contact_title": "Order Administrator",
    "address": "Berguvsvägen  8",
    "city": "Luleå",
    "region": null,
    "postal_code": "S-958 22",
    "country": "Sweden",
    "phone": "0921-12 34 65",
    "fax": "0921-12 34 67"
  },
  {
    "customer_id": "WANDK",
    "company_name": "Die Wandernde Kuh",
    "contact_name": "Rita Müller",
    "contact_title": "Sales Representative",
    "address": "Adenauerallee 900",
    "city": "Stuttgart",
    "region": null,
    "postal_code": "70563",
    "country": "Germany",
    "phone": "0711-020361",
    "fax": "0711-035428"
  }
]
```

**Error:** None

### Case join_009

**Question:** Which products were ordered more than 100 times?

**Text-to-SQL Correct:** False

**Execution Correct:** True

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT p.product_id, p.product_name, COUNT(*) AS order_count FROM order_details od JOIN products p ON od.product_id = p.product_id GROUP BY p.product_id, p.product_name HAVING COUNT(*) > 100
```

**Expected SQL:**

```sql
SELECT products.product_name, COUNT(order_details.order_id) FROM products JOIN order_details ON products.product_id = order_details.product_id GROUP BY products.product_name HAVING COUNT(order_details.order_id) > 100
```

**Expected Rows:**

Showing 0 of 0 rows.

```json
[]
```

**Generated Rows:**

Showing 0 of 0 rows.

```json
[]
```

**Error:** None

### Case join_010

**Question:** What are the top customers by total spending?

**Text-to-SQL Correct:** False

**Execution Correct:** False

**Execution Succeeded:** True

**Generated SQL:**

```sql
SELECT c.customer_id, SUM(od.unit_price * od.quantity * (1 - od.discount)) AS total_spending FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_details od ON o.order_id = od.order_id GROUP BY c.customer_id ORDER BY total_spending DESC
```

**Expected SQL:**

```sql
SELECT customers.company_name, SUM(order_details.unit_price * order_details.quantity) AS total_spent FROM customers JOIN orders ON customers.customer_id = orders.customer_id JOIN order_details ON orders.order_id = order_details.order_id GROUP BY customers.company_name ORDER BY total_spent DESC
```

**Expected Rows:**

Showing first 5 of 89 rows.

```json
[
  {
    "company_name": "QUICK-Stop",
    "total_spent": 117483.390147686
  },
  {
    "company_name": "Save-a-lot Markets",
    "total_spent": 115673.38964271545
  },
  {
    "company_name": "Ernst Handel",
    "total_spent": 113236.67978191376
  },
  {
    "company_name": "Hungry Owl All-Night Grocers",
    "total_spent": 57317.39016246796
  },
  {
    "company_name": "Rattlesnake Canyon Grocery",
    "total_spent": 52245.90034675598
  }
]
```

**Generated Rows:**

Showing first 5 of 89 rows.

```json
[
  {
    "customer_id": "QUICK",
    "total_spending": 110277.30503039382
  },
  {
    "customer_id": "ERNSH",
    "total_spending": 104874.97814367746
  },
  {
    "customer_id": "SAVEA",
    "total_spending": 104361.94954039395
  },
  {
    "customer_id": "RATTC",
    "total_spending": 51097.80082826822
  },
  {
    "customer_id": "HUNGO",
    "total_spending": 49979.90508149549
  }
]
```

**Error:** None
