import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Database:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="motorcraft_system"
        )
        self.cursor = self.db_connection.cursor()

    def commit(self):
        self.db_connection.commit()

    def close(self):
        self.cursor.close()
        self.db_connection.close()

# Inventory System Functions
class Inventory(Database):
    def add_product(self, product_name, product_price, product_stock):
        query = "INSERT INTO products (product_name, product_price, product_stock) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (product_name, product_price, product_stock))
        self.commit()
        print(f"Product {product_name} added successfully!")

    def update_product(self, product_id, product_name, product_price, product_stock):
        query = "UPDATE products SET product_name = %s, product_price = %s, product_stock = %s WHERE product_id = %s"
        self.cursor.execute(query, (product_name, product_price, product_stock, product_id))
        self.commit()
        print(f"Product {product_name} updated successfully!")

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE product_id = %s"
        self.cursor.execute(query, (product_id,))
        self.commit()
        print(f"Product with ID {product_id} deleted successfully!")
        
    def fetch_products(self):
        query = "SELECT * FROM products"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def search_product(self, product_id=None, product_name=None, product_price=None, product_stock=None):
        base_query = "SELECT * FROM products WHERE"
        conditions = []
        values = []

        if product_id is not None:
            conditions.append("product_id = %s")
            values.append(product_id)
        if product_name is not None:
            conditions.append("product_name LIKE %s")
            values.append(f"%{product_name}%")
        if product_price is not None:
            conditions.append("product_price = %s")
            values.append(product_price)
        if product_stock is not None:
            conditions.append("product_stock = %s")
            values.append(product_stock)

        if conditions:
            query = f"{base_query} {' AND '.join(conditions)}"
            self.cursor.execute(query, tuple(values))
            results = self.cursor.fetchall()
            return results
        else:
            print("No search criteria provided.")
            return []




# Account System Functions

class adminAccount(Database):
    def create_account(self, username, password, role='admin'):
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (username, password, role))
        self.commit()
        print(f"Account created for {username}.")

    def login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            print(f"Logged in as {username}")
            return result  # Return user info (user_id, role)
        else:
            print("Invalid username or password.")
            return None


# Inventory GUI       
class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management")
        self.root.geometry("800x600")
        self.root.configure(bg='#212121')

        self.inventory = Inventory()

        # Title Label
        title_label = tk.Label(self.root, text="Inventory Management", fg="#00C853", font=("Verdana", 24, "bold"), bg='#212121')
        title_label.pack(pady=20)

        # Search bar
        search_frame = tk.Frame(self.root, bg='#212121')
        search_frame.pack(pady=10)

        search_label = tk.Label(search_frame, text="Search by ID:", font=("Arial", 12), fg="white", bg='#212121')
        search_label.grid(row=0, column=0, padx=5)

        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=20)
        self.search_entry.grid(row=0, column=1, padx=5)

        search_button = tk.Button(search_frame, text="Search", command=self.search_product, bg="#4CAF50", fg="white", font=("Arial", 12), relief="solid", bd=2)
        search_button.grid(row=0, column=2, padx=5)

        # Product entry form
        form_frame = tk.Frame(self.root, bg='#212121')
        form_frame.pack(pady=10)

        # Add Item Entry Fields
        tk.Label(form_frame, text="Item Name:", font=("Arial", 12), fg="white", bg='#212121').grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Quantity:", font=("Arial", 12), fg="white", bg='#212121').grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Price:", font=("Arial", 12), fg="white", bg='#212121').grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons for Add, Update, Delete
        button_frame = tk.Frame(self.root, bg='#212121')
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Item", command=self.add_item, bg="#4CAF50", fg="white", font=("Arial", 12), relief="solid", bd=2)
        add_button.grid(row=0, column=0, padx=5)

        update_button = tk.Button(button_frame, text="Update Item", command=self.update_item, bg="#FFC107", fg="black", font=("Arial", 12), relief="solid", bd=2)
        update_button.grid(row=0, column=1, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Item", command=self.delete_item, bg="#F44336", fg="white", font=("Arial", 12), relief="solid", bd=2)
        delete_button.grid(row=0, column=2, padx=5)

        # View Inventory Button
        view_button = tk.Button(self.root, text="View Inventory", command=self.view_inventory, bg="#2196F3", fg="white", font=("Arial", 12), relief="solid", bd=2)
        view_button.pack(pady=10)

        # Table Frame for Displaying Inventory
        self.table_frame = tk.Frame(self.root, bg='#212121')
        self.table_frame.pack(pady=20)

        self.inventory_table = ttk.Treeview(self.table_frame, columns=("ID", "Name", "Quantity", "Price"), show='headings')
        self.inventory_table.heading("ID", text="ID")
        self.inventory_table.heading("Name", text="Name")
        self.inventory_table.heading("Quantity", text="Quantity")
        self.inventory_table.heading("Price", text="Price")
        self.inventory_table.pack()

        # Populate the table with all inventory items
        self.populate_inventory()

    def populate_inventory(self):
        """Retrieve all inventory items from the database and display them in the table."""
        products = self.inventory.fetch_products()

        for item in self.inventory_table.get_children():
            self.inventory_table.delete(item)

        for product in products:
            self.inventory_table.insert("", "end", values=product)

    def search_product(self):
        """Search for products by name."""
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showerror("Input Error", "Please enter a search term.")
            return

        products = self.inventory.search_product(search_term)

        # Clear existing rows in the table
        for item in self.inventory_table.get_children():
            self.inventory_table.delete(item)

        if products:
            for product in products:
                self.inventory_table.insert("", "end", values=product)
        else:
            messagebox.showinfo("Not Found", f"No products found with the name: {search_term}")

    def add_item(self):
        """Add a new inventory item."""
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not name or not quantity or not price:
            messagebox.showerror("Input Error", "Please fill out all fields.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            self.inventory.add_product(name, price, quantity)
            messagebox.showinfo("Success", "Item added successfully!")
            self.populate_inventory()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid quantity and price.")

    def update_item(self):
        """Update an existing inventory item."""
        selected_item = self.inventory_table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select an item to update.")
            return

        product_id = self.inventory_table.item(selected_item[0])["values"][0]
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not name or not quantity or not price:
            messagebox.showerror("Input Error", "Please fill out all fields.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            self.inventory.update_product(product_id, name, price, quantity)
            messagebox.showinfo("Success", "Item updated successfully!")
            self.populate_inventory()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid quantity and price.")

    def delete_item(self):
        """Delete an inventory item."""
        selected_item = self.inventory_table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select an item to delete.")
            return

        product_id = self.inventory_table.item(selected_item[0])["values"][0]
        self.inventory.delete_product(product_id)
        messagebox.showinfo("Success", "Item deleted successfully!")
        self.populate_inventory()

    def view_inventory(self):
        """Display the entire inventory."""
        self.populate_inventory()

  

class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("MotoCrafts")
        self.window.geometry("500x500")
        self.window.configure(bg='#212121') 
        

        # Title Label
        title_label = tk.Label(self.window, text="MotoCrafts", fg="#00C853", font=("Verdana", 24, "bold"), bg='#212121')
        title_label.pack(pady=20)

        # Subtitle Label
        subtitle_label = tk.Label(self.window, text="Your Ride, Your Gear, Your Passion", fg="#FFEB3B", font=("Verdana", 14, "italic"), bg='#212121')
        subtitle_label.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self.window, bg='#212121')
        button_frame.pack(pady=50)

        # Admin Button
        admin_button = tk.Button(button_frame, text="Admin", command=self.admin_account, width=15, height=2, 
                                 bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), relief="solid", bd=2)
        admin_button.grid(row=0, column=0, padx=10)

        self.account = adminAccount()  # Initialize Account object for login/signup

        self.window.mainloop()

    def user_account(self):
        # Create a new Toplevel window for user login/signup
        login_window = tk.Toplevel(self.window)
        login_window.title("User Login / Sign Up")
        login_window.geometry("300x300")
        login_window.configure(bg='#f0f0f0')

        # Title label
        title_label = tk.Label(login_window, text="User Login / Sign Up", font=("Arial", 14, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)

        # Username label and entry field
        username_label = tk.Label(login_window, text="Enter Username", font=("Arial", 12), bg='#f0f0f0')
        username_label.pack(pady=5)
        username_entry = tk.Entry(login_window, font=("Arial", 12))
        username_entry.pack(pady=5)

        # Password label and entry field
        password_label = tk.Label(login_window, text="Password", font=("Arial", 12), bg='#f0f0f0')
        password_label.pack(pady=5)
        password_entry = tk.Entry(login_window, font=("Arial", 12), show="*")
        password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(
            login_window, text="Login", width=15, height=2, bg="#008CBA", fg="white", font=("Arial", 12),
            relief="solid", bd=2,
            command=lambda: self.login(username_entry.get(), password_entry.get(), "user")
        )
        login_button.pack(pady=10)

        # Sign-Up button
        signup_button = tk.Button(
            login_window, text="Sign Up", width=15, height=2, bg="#4CAF50", fg="white", font=("Arial", 12),
            relief="solid", bd=2,
            command=lambda: self.sign_up(username_entry.get(), password_entry.get(), "user")
        )
        signup_button.pack(pady=10)

    def admin_account(self):
        # Create a new Toplevel window for admin login/signup
        login_window = tk.Toplevel(self.window)
        login_window.title("Admin Login / Sign Up")
        login_window.geometry("300x300")
        login_window.configure(bg='#f0f0f0')

        # Title label
        title_label = tk.Label(login_window, text="Admin Login / Sign Up", font=("Arial", 14, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)

        # Username label and entry field
        username_label = tk.Label(login_window, text="Enter Username", font=("Arial", 12), bg='#f0f0f0')
        username_label.pack(pady=5)
        username_entry = tk.Entry(login_window, font=("Arial", 12))
        username_entry.pack(pady=5)

        # Password label and entry field
        password_label = tk.Label(login_window, text="Password", font=("Arial", 12), bg='#f0f0f0')
        password_label.pack(pady=5)
        password_entry = tk.Entry(login_window, font=("Arial", 12), show="*")
        password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(
            login_window, text="Login", width=15, height=2, bg="#008CBA", fg="white", font=("Arial", 12),
            relief="solid", bd=2,
            command=lambda: self.login(username_entry.get(), password_entry.get(), "admin")
        )
        login_button.pack(pady=10)

        # Sign-Up button
        signup_button = tk.Button(
            login_window, text="Sign Up", width=15, height=2, bg="#4CAF50", fg="white", font=("Arial", 12),
            relief="solid", bd=2,
            command=lambda: self.sign_up(username_entry.get(), password_entry.get(), "admin")
        )
        signup_button.pack(pady=10)

    def login(self, username, password, expected_role):
        # Check if the username and password are provided
        if not username or not password:
            messagebox.showerror("Input Error", "Username and Password cannot be empty.")
            return None

        # Query to verify user credentials and role
        query = "SELECT * FROM users WHERE username = %s AND password = %s AND role = %s"
        self.account.cursor.execute(query, (username, password, expected_role))
        result = self.account.cursor.fetchone()

        if result:
            user_id, role = result[0], result[2]
            messagebox.showinfo("Login Successful", f"Logged in as {role}: {username}")
            self.open_inventory()
            self.root.destroy()  # Close login window
                
                
            # Optionally, you can add other windows for different roles here
            # For example, a user role could open a different window like PurchaseGUI

        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_inventory(self):
        # Initialize the main Tkinter window for Inventory GUI
        inventory_root = tk.Tk()
        InventoryGUI(inventory_root)  # Pass the new Tk root to InventoryGUI
        inventory_root.mainloop()


    def sign_up(self, username, password, role):
        # Validate inputs
        if not username or not password:
            messagebox.showerror("Sign Up Failed", "Username and password cannot be empty.")
            return

        # Check if username already exists
        query_check = "SELECT * FROM users WHERE username = %s"
        self.account.cursor.execute(query_check, (username,))
        if self.account.cursor.fetchone():
            messagebox.showerror("Sign Up Failed", "Username already exists.")
            return

        # Insert new user into the database
        query_insert = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        try:
            self.account.cursor.execute(query_insert, (username, password, role))
            self.account.commit()
            messagebox.showinfo("Sign Up Successful", f"Account created for {username} as {role}.")
        except Exception as e:
            messagebox.showerror("Sign Up Failed", f"Error creating account: {e}")


        self.window.mainloop()

# Main logic to run the app
gui = Interface()



