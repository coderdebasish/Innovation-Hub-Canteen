import tkinter as tk
from tkinter import ttk, messagebox
import os
from canteen_backend import ItemManager, InvoiceGenerator, Auth

class CanteenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Innovation Hub Canteen")
        self.root.geometry("900x600")
        
        self.item_manager = ItemManager()
        self.invoice_generator = InvoiceGenerator()
        
        self.cart = [] # List of dicts
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.tab_billing = ttk.Frame(self.notebook)
        self.tab_inventory = ttk.Frame(self.notebook)
        self.tab_admin = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_billing, text='Billing')
        self.notebook.add(self.tab_inventory, text='Inventory')
        self.notebook.add(self.tab_admin, text='Admin Panel')
        
        self.setup_billing_tab()
        self.setup_inventory_tab()
        self.setup_admin_tab()

    def setup_billing_tab(self):
        # --- Input Section ---
        input_frame = ttk.LabelFrame(self.tab_billing, text="Add Item")
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Item Code:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_code = ttk.Entry(input_frame)
        self.entry_code.grid(row=0, column=1, padx=5, pady=5)
        self.entry_code.bind('<Return>', lambda e: self.focus_qty())
        
        ttk.Label(input_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_qty = ttk.Entry(input_frame, width=5)
        self.entry_qty.grid(row=0, column=3, padx=5, pady=5)
        self.entry_qty.bind('<Return>', lambda e: self.add_to_cart())
        
        self.btn_add = ttk.Button(input_frame, text="Add to Cart", command=self.add_to_cart)
        self.btn_add.grid(row=0, column=4, padx=10, pady=5)
        
        # --- Cart Section ---
        cart_frame = ttk.LabelFrame(self.tab_billing, text="Cart")
        cart_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        columns = ('code', 'name', 'price', 'qty', 'total')
        self.tree_cart = ttk.Treeview(cart_frame, columns=columns, show='headings')
        self.tree_cart.heading('code', text='Code')
        self.tree_cart.heading('name', text='Item Name')
        self.tree_cart.heading('price', text='Price')
        self.tree_cart.heading('qty', text='Qty')
        self.tree_cart.heading('total', text='Total')
        
        self.tree_cart.column('code', width=80)
        self.tree_cart.column('name', width=200)
        self.tree_cart.column('price', width=80)
        self.tree_cart.column('qty', width=60)
        self.tree_cart.column('total', width=80)
        
        self.tree_cart.pack(expand=True, fill='both', padx=5, pady=5)
        
        # --- Actions Section ---
        action_frame = ttk.LabelFrame(self.tab_billing, text="Checkout")
        action_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(action_frame, text="Discount:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_discount = ttk.Entry(action_frame, width=10)
        self.entry_discount.insert(0, "0")
        self.entry_discount.grid(row=0, column=1, padx=5, pady=5)
        
        self.var_paymode = tk.StringVar(value="Cash")
        ttk.Radiobutton(action_frame, text="Cash", variable=self.var_paymode, value="Cash").grid(row=0, column=2, padx=5)
        ttk.Radiobutton(action_frame, text="UPI", variable=self.var_paymode, value="UPI").grid(row=0, column=3, padx=5)
        
        self.lbl_total = ttk.Label(action_frame, text="Grand Total: 0", font=('Arial', 12, 'bold'))
        self.lbl_total.grid(row=0, column=4, padx=20, pady=5)
        
        btn_gen = ttk.Button(action_frame, text="Generate Invoice", command=self.generate_invoice)
        btn_gen.grid(row=0, column=5, padx=10, pady=5)

        btn_clear = ttk.Button(action_frame, text="Clear Cart", command=self.clear_cart)
        btn_clear.grid(row=0, column=6, padx=5)

    def focus_qty(self):
        self.entry_qty.focus()

    def add_to_cart(self):
        code = self.entry_code.get().strip()
        qty_str = self.entry_qty.get().strip()
        
        if not code or not qty_str:
            messagebox.showerror("Error", "Please enter Code and Quantity")
            return
            
        if not qty_str.isdigit():
            messagebox.showerror("Error", "Quantity must be a number")
            return
            
        qty = int(qty_str)
        if qty <= 0:
            messagebox.showerror("Error", "Quantity must be > 0")
            return

        if len(self.cart) >= 8:
             messagebox.showerror("Error", "Max 8 items allowed per invoice.")
             return

        item = self.item_manager.get_item(code)
        if not item:
            messagebox.showerror("Error", "Item not found!")
            return
            
        if item['stock'] < qty:
            messagebox.showerror("Error", f"Insufficient Stock! Available: {item['stock']}")
            return
            
        # Add to cart logic
        total = item['price'] * qty
        cart_item = {
            'code': code,
            'name': item['name'],
            'price': item['price'],
            'qty': qty,
            'total': total
        }
        self.cart.append(cart_item)
        self.tree_cart.insert('', 'end', values=(code, item['name'], item['price'], qty, total))
        
        self.update_total()
        self.entry_code.delete(0, 'end')
        self.entry_qty.delete(0, 'end')
        self.entry_code.focus()

    def update_total(self):
        total = sum(i['total'] for i in self.cart)
        try:
            discount = int(self.entry_discount.get())
        except ValueError:
            discount = 0
        self.lbl_total.config(text=f"Grand Total: {total - discount}")

    def clear_cart(self):
        self.cart = []
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)
        self.update_total()

    def generate_invoice(self):
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
            
        try:
            discount = int(self.entry_discount.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Discount")
            return
            
        pay_mode = self.var_paymode.get()
        
        # Check stock again before finalizing
        for cart_item in self.cart:
            db_item = self.item_manager.get_item(cart_item['code'])
            if db_item['stock'] < cart_item['qty']:
                messagebox.showerror("Error", f"Stock changed for {cart_item['name']}. Not enough stock.")
                return

        try:
            # Update stock
            for cart_item in self.cart:
                self.item_manager.update_stock(cart_item['code'], cart_item['qty'])
            
            # Generate Doc
            path = self.invoice_generator.generate_invoice(self.cart, discount, pay_mode)
            
            messagebox.showinfo("Success", f"Invoice Generated!\nSaved to: {path}")
            os.startfile(path) # Open the file
            
            self.clear_cart()
            self.refresh_inventory() # Update inventory tab
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def setup_inventory_tab(self):
        # Toolbar
        toolbar = ttk.Frame(self.tab_inventory)
        toolbar.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(toolbar, text="Refresh", command=self.refresh_inventory).pack(side='left')
        
        # Table
        columns = ('code', 'name', 'price', 'stock')
        self.tree_inv = ttk.Treeview(self.tab_inventory, columns=columns, show='headings')
        self.tree_inv.heading('code', text='Code')
        self.tree_inv.heading('name', text='Name')
        self.tree_inv.heading('price', text='Price')
        self.tree_inv.heading('stock', text='Stock')
        self.tree_inv.pack(expand=True, fill='both', padx=10, pady=5)
        
        self.refresh_inventory()

    def refresh_inventory(self):
        for item in self.tree_inv.get_children():
            self.tree_inv.delete(item)
            
        items = self.item_manager.get_all_items()
        for item in items:
            self.tree_inv.insert('', 'end', values=(item['code'], item['name'], item['price'], item['stock']))

    def setup_admin_tab(self):
        self.admin_login_frame = ttk.Frame(self.tab_admin)
        self.admin_login_frame.pack(expand=True)
        
        ttk.Label(self.admin_login_frame, text="Admin Password:").pack(pady=5)
        self.entry_admin_pass = ttk.Entry(self.admin_login_frame, show="*")
        self.entry_admin_pass.pack(pady=5)
        ttk.Button(self.admin_login_frame, text="Login", command=self.admin_login).pack(pady=10)
        
        self.admin_panel_frame = ttk.Frame(self.tab_admin)
        # Hidden initially

    def admin_login(self):
        pwd = self.entry_admin_pass.get()
        if Auth.verify_admin(pwd):
            self.admin_login_frame.pack_forget()
            self.show_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid Password")

    def show_admin_panel(self):
        self.admin_panel_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Add Item
        frame_add = ttk.LabelFrame(self.admin_panel_frame, text="Add New Item")
        frame_add.pack(fill='x', pady=10)
        
        ttk.Label(frame_add, text="Code:").grid(row=0, column=0, padx=5)
        self.add_code = ttk.Entry(frame_add, width=10)
        self.add_code.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_add, text="Name:").grid(row=0, column=2, padx=5)
        self.add_name = ttk.Entry(frame_add)
        self.add_name.grid(row=0, column=3, padx=5)
        
        ttk.Label(frame_add, text="Price:").grid(row=0, column=4, padx=5)
        self.add_price = ttk.Entry(frame_add, width=10)
        self.add_price.grid(row=0, column=5, padx=5)
        
        ttk.Label(frame_add, text="Stock:").grid(row=0, column=6, padx=5)
        self.add_stock = ttk.Entry(frame_add, width=10)
        self.add_stock.grid(row=0, column=7, padx=5)
        
        ttk.Button(frame_add, text="Add Item", command=self.admin_add_item).grid(row=0, column=8, padx=10)

        # Update Stock (Simplified)
        frame_stock = ttk.LabelFrame(self.admin_panel_frame, text="Update Stock (Overwrite)")
        frame_stock.pack(fill='x', pady=10)
        
        ttk.Label(frame_stock, text="Code:").grid(row=0, column=0, padx=5)
        self.upd_code = ttk.Entry(frame_stock, width=10)
        self.upd_code.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_stock, text="New Stock:").grid(row=0, column=2, padx=5)
        self.upd_stock = ttk.Entry(frame_stock, width=10)
        self.upd_stock.grid(row=0, column=3, padx=5)
        
        ttk.Button(frame_stock, text="Update", command=self.admin_update_stock).grid(row=0, column=4, padx=10)

    def admin_add_item(self):
        code = self.add_code.get()
        name = self.add_name.get()
        price = self.add_price.get()
        stock = self.add_stock.get()
        
        if not (code and name and price and stock):
            messagebox.showerror("Error", "All fields required")
            return
            
        if self.item_manager.get_item(code):
            messagebox.showerror("Error", "Item code already exists")
            return
            
        try:
            self.item_manager.save_item(code, name, int(price), int(stock))
            messagebox.showinfo("Success", "Item Added")
            self.refresh_inventory()
            # Clear fields
            self.add_code.delete(0, 'end')
            self.add_name.delete(0, 'end')
            self.add_price.delete(0, 'end')
            self.add_stock.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Price and Stock must be numbers")

    def admin_update_stock(self):
        code = self.upd_code.get()
        stock = self.upd_stock.get()
        
        item = self.item_manager.get_item(code)
        if not item:
            messagebox.showerror("Error", "Item not found")
            return
            
        try:
            self.item_manager.save_item(code, item['name'], item['price'], int(stock))
            messagebox.showinfo("Success", "Stock Updated")
            self.refresh_inventory()
            self.upd_code.delete(0, 'end')
            self.upd_stock.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Stock must be a number")

if __name__ == "__main__":
    root = tk.Tk()
    app = CanteenApp(root)
    root.mainloop()
