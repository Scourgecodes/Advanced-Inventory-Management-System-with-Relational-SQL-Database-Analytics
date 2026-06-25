import sqlite3
from datetime import datetime

class InventoryDB:
    def __init__(self, db_name="warehouse.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Enable Foreign Key support in SQLite
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()

    def create_tables(self):
        """Creates relational tables with constraints."""
        # Table 1: Products Stock
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                cost_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0),
                low_stock_threshold INTEGER DEFAULT 5
            )
        """)

        # Table 2: Sales Ledger linked via Foreign Key
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity_sold INTEGER NOT NULL CHECK(quantity_sold > 0),
                total_revenue REAL NOT NULL,
                sale_date TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def close(self):
        self.conn.close()


class InventoryManager:
    def __init__(self):
        self.db = InventoryDB()

    def add_product(self, sku, name, cost, selling, stock, threshold):
        """Inserts a new product record into the database."""
        try:
            self.db.cursor.execute("""
                INSERT INTO products (sku, name, cost_price, selling_price, stock_quantity, low_stock_threshold)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (sku.upper(), name, cost, selling, stock, threshold))
            self.db.conn.commit()
            print(f"Success: Product '{name}' added successfully under SKU: {sku.upper()}.")
        except sqlite3.IntegrityError:
            print(f"Database Error: A product with SKU '{sku.upper()}' already exists.")

    def process_sale(self, sku, quantity):
        """Advanced transactional logic: validates stock, processes deduction, updates ledger."""
        try:
            # 1. Fetch item and check current stock level
            self.db.cursor.execute("SELECT product_id, name, selling_price, stock_quantity FROM products WHERE sku = ?", (sku.upper(),))
            product = self.db.cursor.fetchone()

            if not product:
                print("Error: Product SKU not found in system.")
                return

            p_id, name, selling_price, current_stock = product

            if current_stock < quantity:
                print(f"Transaction Rejected: Insufficient stock. Available stock for {name} is {current_stock} units.")
                return

            # 2. Execute SQL updates safely inside a transaction block
            new_stock = current_stock - quantity
            total_revenue = selling_price * quantity
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Deduct stock
            self.db.cursor.execute("UPDATE products SET stock_quantity = ? WHERE product_id = ?", (new_stock, p_id))
            # Record sale transaction
            self.db.cursor.execute("""
                INSERT INTO sales (product_id, quantity_sold, total_revenue, sale_date)
                VALUES (?, ?, ?, ?)
            """, (p_id, quantity, total_revenue, timestamp))

            self.db.conn.commit()
            print(f"Transaction Complete: Sold {quantity} units of '{name}'. Total Revenue collected: ${total_revenue:.2f}")

        except sqlite3.Error as e:
            self.db.conn.rollback()
            print(f"Transaction Failed. Database rolled back safely. Error: {e}")

    def list_inventory(self):
        """Displays all items in the inventory database."""
        self.db.cursor.execute("SELECT product_id, sku, name, selling_price, stock_quantity FROM products")
        items = self.db.cursor.fetchall()
        
        if not items:
            print("Inventory database is currently empty.")
            return

        print("\n" + "="*60)
        print(f"{'ID':<4} | {'SKU':<10} | {'Product Name':<20} | {'Price':<10} | {'Stock Remaining'}")
        print("="*60)
        for item in items:
            print(f"{item[0]:<4} | {item[1]:<10} | {item[2]:<20} | ${item[3]:<9.2f} | {item[4]}")
        print("="*60)

    def view_low_stock_alerts(self):
        """Aggregates items where stock levels drop below custom thresholds."""
        self.db.cursor.execute("SELECT sku, name, stock_quantity, low_stock_threshold FROM products WHERE stock_quantity <= low_stock_threshold")
        alerts = self.db.cursor.fetchall()

        if not alerts:
            print("Excellent: All items are securely stocked above thresholds.")
            return

        print("\n🚨 LOW STOCK ALERT SYSTEM 🚨")
        for alert in alerts:
            print(f"⚠️ SKU: {alert[0]} | Item: {alert[1]} | Current Stock: {alert[2]} (Critical Threshold Limit: {alert[3]})")

    def display_business_analytics(self):
        """Advanced analytical logic: Joins tables and aggregates metrics via SQL formulas."""
        print("\n=== BUSINESS REAL-TIME DATA ANALYTICS ===")
        
        # 1. Total revenue collected across all records
        self.db.cursor.execute("SELECT SUM(total_revenue) FROM sales")
        total_rev = self.db.cursor.fetchone()[0] or 0.0

        # 2. Total unit sales count
        self.db.cursor.execute("SELECT SUM(quantity_sold) FROM sales")
        total_units = self.db.cursor.fetchone()[0] or 0

        # 3. Complex relational SQL query to compute actual net business profit margins
        # (Selling Price - Cost Price) * Quantity Sold from joined tables
        self.db.cursor.execute("""
            SELECT SUM((p.selling_price - p.cost_price) * s.quantity_sold)
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
        """)
        total_profit = self.db.cursor.fetchone()[0] or 0.0

        print(f"📈 Gross Accumulated Revenue: ${total_rev:.2f}")
        print(f"📦 Total Product Units Sold:  {total_units} units")
        print(f"💰 Net Operational Profit:    ${total_profit:.2f}")
        print("=========================================")


if __name__ == "__main__":
    manager = InventoryManager()
    
    while True:
        print("\n--- Advanced SQL Inventory Enterprise System ---")
        print("1. Register New Product Row")
        print("2. Record System Sale Transaction")
        print("3. Fetch Complete Inventory Records")
        print("4. Inspect Low Stock Alerts")
        print("5. Generate Business Financial Analytics")
        print("6. Exit Database Engine")
        
        choice = input("Select system operational mode (1-6): ").strip()
        
        if choice == "1":
            sku = input("Enter Product Unique SKU Code (e.g., LAP101): ")
            name = input("Enter Product Descriptive Name: ")
            cost = float(input("Enter Unit Cost Price: "))
            selling = float(input("Enter Unit Market Selling Price: "))
            stock = int(input("Enter Initial Base Stock Volume: "))
            threshold = int(input("Enter Low Stock Automated Alert Threshold: "))
            manager.add_product(sku, name, cost, selling, stock, threshold)
            
        elif choice == "2":
            sku = input("Enter Product SKU Code to process sale: ")
            qty = int(input("Enter Quantity Units Sold: "))
            manager.process_sale(sku, qty)
            
        elif choice == "3":
            manager.list_inventory()
            
        elif choice == "4":
            manager.view_low_stock_alerts()
            
        elif choice == "5":
            manager.display_business_analytics()
            
        elif choice == "6":
            print("Closing database connections safely. Goodbye!")
            manager.db.close()
            break
        else:
            print("Invalid system input. Select options from 1 to 6.") 
