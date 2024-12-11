from datetime import datetime

from database.auth_dao import AuthDAO
import database.model.menuitem
from database.model import menuitem
from database.model.order import Order
from database.model.orderdetail import OrderDetail
from utils.appearance import *
import tkinter as tk
from tkinter import font as tkfont, ttk
from PIL import Image, ImageTk

from utils.load_image import load_image

CUSTOM_FONT_PROPERTIES = {
    "family": "Helvetica",
    "size": 13,
    "weight": "bold"
}

class OrderContent:

    def __init__(self, master, user):
        self.master = master
        self._user = user

        self._temp_orderdetails = []
        self._selected_item_index = None

        # Create the left panel (body_panel)
        self.body_panel = tk.Frame(self.master)
        self.body_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a Label to the body_panel (this part is static)
        tk.Label(self.body_panel, text="Menu", font=tkfont.Font(**CUSTOM_FONT_PROPERTIES)).pack(pady=20)

        # Create a frame for the scrollable content
        self.scrollable_frame = tk.Frame(self.body_panel)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Canvas for the scrollable table_frame
        self.canvas = tk.Canvas(self.scrollable_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configure the canvas to respond to the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a frame inside the canvas for the table_frame content
        self.table_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Bind scroll events for Windows/Mac and Linux
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # For Windows and MacOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)    # For Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)    # For Linux scroll down

        # Populate the table_frame
        self._create_body_content(self.table_frame)

        # Create the right panel (body_panel_right)
        self.body_panel_right = tk.Frame(self.master, bg="blue")
        self.body_panel_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        self.body_panel_right_bottom = tk.Frame(self.body_panel_right, bg="green")
        self.body_panel_right_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.body_panel_right_top = tk.Frame(self.body_panel_right, bg="brown")
        self.body_panel_right_top.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        self._create_body_right_content(self.body_panel_right_top)
        self._create_crud_panel(5, 10, self.body_panel_right_bottom)

    def _on_mousewheel(self, event):
        # Windows and MacOS
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            # Linux
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def _create_body_content(self, panel):

        self._data = database.model.menuitem.MenuItem.get_all()

        items_per_row = 4  # Number of items per row

        for index, item in enumerate(self._data):
            # Calculate the row and column index
            row = index // items_per_row
            column = index % items_per_row

            if item.image != "":
                photo = load_image(f"assets/menuitem/{item.image}", size=(200, 200))
            else:
                photo = load_image(f"assets/img.png", size=(260, 200))

            # Create a button with image and text
            btn = tk.Button(panel,
                            text=f"\n {item.name} \n ${item.price} \n", justify='center',
                            compound=tk.TOP,
                            image=photo,
                            font=tkfont.Font(**CUSTOM_FONT_PROPERTIES),
                            width=250, height=360, bg="white")

            # Keep a reference to the image to prevent garbage collection
            btn.image = photo

            # Bind the button click event to add the item to _temp_orderdetails
            btn.config(command=lambda i=item: self._btn_add_temp_order_details(i))

            # Place the button in the grid at the calculated row and column
            btn.grid(row=row, column=column, padx=10, pady=10)

    def _btn_add_temp_order_details(self, item):
        """
        Add the selected MenuItem to _temp_orderdetails or increase the quantity if it already exists.
        """
        # Default quantity for now, can be set by user input
        quantity = 1
        price = item.price

        # Check if the item is already in _temp_orderdetails
        found = False
        for order_detail in self._temp_orderdetails:
            if order_detail.menuitem == item:
                # Item already exists, increase the quantity
                order_detail.qty += quantity
                order_detail.price += price
                found = True
                break

        if not found:
            # If the item is not found, create a new OrderDetail and add it
            order_detail = OrderDetail(None, None, item, quantity, item.price)
            self._temp_orderdetails.append(order_detail)

        # Optional: print the current _temp_orderdetails for debugging
        print(f"Added {item.name} to order details. Current order details:")
        for od in self._temp_orderdetails:
            print(od)

        # Update the Treeview with the new _temp_orderdetails
        self._populate_treeview()

    def _create_body_right_content(self, panel):
        tk.Label(panel, text="Order", font=tkfont.Font(**CUSTOM_FONT_PROPERTIES)).pack(pady=20)
        self.table_frame_right = tk.Frame(panel, height=400)
        self.table_frame_right.pack(fill=tk.BOTH, side=tk.TOP)

        self.tree = ttk.Treeview(self.table_frame_right, columns=("Index", "Name", "Price", "Qty", "Total", "Image"))
        style = ttk.Style()
        style.configure("Treeview", rowheight=150)
        self.myfont = (tkfont.Font(**HEADER_FONT_PROPERTIES))
        style.configure("Treeview.Heading",
                        font=(self.myfont))

        self.tree.heading("#0", text="Image", anchor=tk.CENTER)
        self.tree.heading("Index", text="Index", anchor=tk.CENTER)
        self.tree.heading("Name", text="Name", anchor=tk.CENTER)
        self.tree.heading("Price", text="Price", anchor=tk.CENTER)
        self.tree.heading("Qty", text="Qty", anchor=tk.CENTER)
        self.tree.heading("Total", text="Total", anchor=tk.CENTER)
        self.tree.heading("Image", text="Image")

        self.tree.column("#0", width=150, anchor=tk.CENTER)
        self.tree.column("Index", width=0, stretch=tk.NO)
        self.tree.column("Name", anchor=tk.CENTER)
        self.tree.column("Price", anchor=tk.CENTER)
        self.tree.column("Qty", anchor=tk.CENTER)
        self.tree.column("Total", anchor=tk.CENTER)
        self.tree.column("Image", width=0, stretch=tk.NO)

        # Create vertical and horizontal scrollbars
        vsb = ttk.Scrollbar(self.table_frame_right, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame_right, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Pack the Treeview and scrollbars
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # List to keep references to PhotoImage objects
        self.photos = []

        # Define tags for row colors
        self.tree.tag_configure("even_row", background="gray80")
        self.tree.tag_configure("odd_row", background="gray90")

        # Define tag for row font style
        self.tree.tag_configure("row_tag", font=tkfont.Font(**ROW_FONT_PROPERTIES))
        # Load images and insert data into the Treeview

        self._populate_treeview()

        self.tree.bind('<<TreeviewSelect>>', self._on_item_selected)

    def _populate_treeview(self):
        # Clear existing items and images
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.photos.clear()

        try:
            self._data = self._temp_orderdetails
        except Exception as e:
            print(f"Database Error: {e}")
            self._data = []

        # Print status
        if not self._data:  # Check if the list is empty
            print("No menu items found.")
        else:
            print("Menu Items retrieved successfully:")

        # Load images and insert data into the Treeview
        for i, item in enumerate(self._data):
            try:
                image_path = MENUITEM_IMG_PATH + item.menuitem.image if item.menuitem.image else IMG_PATH

                # Use the load_image function to load and resize the image
                try:
                    photo = load_image(image_path, size=(140, 140))  # Adjust size as needed
                except FileNotFoundError:
                    # Fallback to default image if file not found
                    photo = load_image(IMG_PATH, size=(140, 140))

                self.photos.append(photo)  # Keep a reference to the image

                # Determine row tag based on index
                item_tag = "even_row" if i % 2 == 0 else "odd_row"

                # Insert item into the Treeview
                item_id = self.tree.insert("", "end", text="", image=photo,
                                           values=(i, item.menuitem.name, f"$ {item.menuitem.price}", item.qty, f"$ {item.price}", item.menuitem.image))
                self.tree.item(item_id, tags=("row_tag", item_tag))

            except Exception as e:
                print(f"Image Error: {e}")

    def _on_item_selected(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item['values']
            self._selected_item_index = values[0]
            print(f"Selected item: {self._selected_item_index}")

    def _create_crud_panel(self, _PADX, _PADY, panel):
        # Create a new frame for CRUD buttons
        self.right_nav_panel_bottom = tk.Frame(panel, bg="white")
        self.right_nav_panel_bottom.pack(fill=tk.BOTH, pady=_PADY, padx=_PADX)

        # Pack buttons side by side

        self.void_button = tk.Button(self.right_nav_panel_bottom, text="Void",
                                       font=tkfont.Font(**ENTRY_FONT_PROPERTIES), bg="salmon",
                                       command=self._void_btn)
        self.void_button.pack(side=tk.BOTTOM, expand=True, fill=tk.X, padx=_PADX // 2)

        self.total_button = tk.Button(self.right_nav_panel_bottom, text="Total",
                                       font=tkfont.Font(**ENTRY_FONT_PROPERTIES), bg="lightgreen",
                                       command=self._total_btn)
        self.total_button.pack(side=tk.BOTTOM, expand=True, fill=tk.X, padx=_PADX // 2)

        self.remove_button = tk.Button(self.right_nav_panel_bottom, text="Remove",
                                       font=tkfont.Font(**ENTRY_FONT_PROPERTIES), bg="lightblue",
                                       command=self._remove_btn)
        self.remove_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=_PADX // 2)

        self.removes_button = tk.Button(self.right_nav_panel_bottom, text="Removes",
                                       font=tkfont.Font(**ENTRY_FONT_PROPERTIES), bg="yellow",
                                       command=self._removes_btn)
        self.removes_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=_PADX // 2)

    def _total_btn(self):
        try:
            # Validate if user exists
            if not AuthDAO.check_if_user_exists(self._user['username']):
                return

            # Calculate total price
            total_price = sum(item.price for item in self._temp_orderdetails)

            # Create new order
            new_order = Order(employee_id=self._user['id'], date=datetime.now(), cost=total_price)
            new_order_id = new_order.save()
            new_order.id = new_order_id

            # Save order details
            for item in self._temp_orderdetails:
                item.order = new_order
                item.save()

            print(f"Order saved with ID: {new_order_id}")
            self._void_btn()

        except Exception as e:
            print(f"An error occurred: {e}")

    def _remove_btn(self):
        index_to_remove = None
        # Check if _selected_item_index attribute exists
        if hasattr(self, '_selected_item_index'):
            if self._selected_item_index is not None:
                index_to_remove = self._selected_item_index
                if index_to_remove is not None:
                    # Ensure the index is within range
                    if 0 <= index_to_remove < len(self._temp_orderdetails):
                        # Get the item to remove
                        order_detail = self._temp_orderdetails[index_to_remove]

                        # Subtract the quantity from the item
                        if order_detail.qty > 1:
                            order_detail.qty -= 1
                            print(f"Reduced quantity of {order_detail.menuitem.name} to {order_detail.qty}")

                        # If the quantity reaches 0, remove the item from the list
                        else:
                            self._removes_btn()

                        # Update the Treeview
                        self._populate_treeview()
                    else:
                        print("Selected item index is out of range.")
                else:
                    print("No item selected or index is not set.")
            else:
                print("_selected_item_index is None.")
        else:
            print("_selected_item_index attribute does not exist.")

    def _removes_btn(self):
        if hasattr(self, '_selected_item_index'):
            # Remove the item from _temp_orderdetails
            index_to_remove = self._selected_item_index
            if 0 <= index_to_remove < len(self._temp_orderdetails):
                removed_item = self._temp_orderdetails.pop(index_to_remove)
                print(f"Removed item: {removed_item.menuitem.name}")

                # Update the Treeview
                self._populate_treeview()

                # Clear selected item index
                del self._selected_item_index
                self._populate_treeview()
            else:
                print("Selected item index is out of range.")
        else:
            print("No item selected.")

    def _void_btn(self):
        self._temp_orderdetails = []
        self._populate_treeview()

    def destroy(self):
        for widget in self.body_panel.winfo_children():
            widget.destroy()
        self.body_panel.destroy()

        for widget in self.body_panel_right.winfo_children():
            widget.destroy()
        self.body_panel_right.destroy()
