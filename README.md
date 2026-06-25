# Advanced SQL Inventory Management & Business Analytics System

An enterprise-grade command-line application built to handle product tracking, relational data persistence, automated sales transactions, and real-time financial reporting. This system connects Python directly to a relational SQLite database engine, replacing flat text or JSON storage files with production-ready database logic.

---

## 📊 Core System Features

* **Relational Database Architecture:** Uses a two-table relational structure linking a live transaction sales ledger to a primary product stock catalog using strict Foreign Keys.
* **Data Integrity Guardrails:** Implements integrated SQL constraints (CHECK constraints) to block invalid inputs, preventing negative stock levels or invalid sales data.
* **Atomic Transaction Safety:** Implements structured database commit and rollback routines (conn.rollback()). If an error or system crash occurs mid-sale, the database safely rolls back to prevent data corruption.
* **Real-Time Financial Aggregations:** Uses complex SQL query joins and mathematical aggregation formulas to calculate gross revenue, unit volume sales, and net operational profit margins on the fly.
* **Automated Low-Stock Alerts:** Features a dedicated warning engine that scans stock levels against customizable threshold limits to flag items that need immediate restocking.

---

## 🛠️ Technology Stack

* **Language Platform:** Python 3
* **Database Engine:** Native SQLite3 (Relational Database Management System)
* **Core Modules:** datetime (for real-time transaction timestamping)

---

## 🗄️ Database Schema Design

The system automatically manages a database file named warehouse.db with the following structural layout:

### 1. products Table (Stock Catalog)
* product_id: Integer, Primary Key (Auto-Increment)
* sku: Text, Unique, Not Null (e.g., LAP101)
* name: Text, Not Null
* cost_price: Real, Not Null (Wholesale price paid to buy the item)
* selling_price: Real, Not Null (Retail retail price customers pay)
* stock_quantity: Integer, Not Null (Must be >= 0)
* low_stock_threshold: Integer, Default 5 (Trigger point for warnings)

### 2. sales Table (Transaction Ledger)
* sale_id: Integer, Primary Key (Auto-Increment)
* product_id: Integer, Foreign Key (References products.product_id with ON DELETE CASCADE)
* quantity_sold: Integer, Not Null (Must be > 0)
* total_revenue: Real, Not Null (Calculated as selling_price * quantity_sold)
* sale_date: Text, Not Null (Automated system timestamp)

---

## 🚀 Installation & Operational Guide

### Step 1: Initialize Your Terminal
Open your Anaconda Prompt or standard system terminal.

### Step 2: Navigate to Your Workspace
Route your terminal path to your project folder where the script is located:

    cd OneDrive\Desktop\AI_Agents

### Step 3: Run the Application
Execute the python script to boot the system command-line interface:

    python inventory_system.py

*(Note: The system will automatically generate a clean warehouse.db file in this folder the very first time it runs. You do not need to create or upload a database file manually.)*

---

## 🕹️ System Operation Guide

When running the application, you will interact with an interactive 6-option system menu:

1. **Register New Product Row:** Prompts you for a unique SKU, descriptive name, financial pricing (cost vs. selling), and current inventory quantity. It handles duplicate SKU rejections natively.
2. **Record System Sale Transaction:** Processes a customer purchase. Input the SKU and quantity. The system automatically verifies if there is enough stock, calculates the revenue, deducts the items from inventory, and records the sale entry simultaneously.
3. **Fetch Complete Inventory Records:** Queries and builds a clean formatted table showing all items, current pricing, and active quantities available in the warehouse.
4. **Inspect Low Stock Alerts:** Scans the entire stock list and pulls a summary of all items whose quantity matches or drops below their set threshold limits.
5. **Generate Business Financial Analytics:** Runs data formulas across both relational tables to instantly output your total gross revenue, overall product units sold, and clear net profit margins.
6. **Exit Database Engine:** Closes active database read/write connections cleanly and safely terminates the system execution loops.

---

## 🔄 Technical Data Pipeline Map

    [User Input Interface] 
             ⬇️
    [System Validation Engine] (Checks inputs & stock volumes)
             ⬇️
    [SQLite Relational Engine] (Executes structured SQL queries)
             ⬇️
    [Relational Transaction Commit / Rollback] (Protects data integrity)
             ⬇️
    [Terminal Interface Output / Financial Dashboard Reports]
