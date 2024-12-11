import tkinter as tk
from tkinter import ttk
import database.model.menuitem
import database.model.order
from utils.appearance import *
import tkinter.font as tkfont


class ReportContent:

    def __init__(self, master):
        self._selected_id = None
        self._selected_image_path = ""
        self._image_path = "assets/menuitem/"

        self.master = master

        self.body_panel = tk.Frame(self.master, bg="red")
        self.body_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._create_body_content(self.body_panel)

        # self.body_panel_2 = tk.Frame(self.master, bg="red")
        # self.body_panel_2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        #self._create_body_content_2(self.body_panel_2)

    def _create_body_content(self, panel):
        # Add content to the body panel
        tk.Label(panel, text="Report Invoice", font=tkfont.Font(**CUSTOM_FONT_PROPERTIES)).pack(pady=20)

        # Create a frame for the table
        self.table_frame = tk.Frame(panel)
        self.table_frame.pack(expand=True, fill=tk.BOTH)

        try:
            self._data = database.model.order.Order.get_all()
        except Exception as e:
            print(f"Database Error: {e}")
            self._data = []

        # Print status
        if not self._data:  # Check if the list is empty
            print("No menu items found.")
        else:
            print("Menu Items retrieved successfully:")

        # Create a Treeview widget
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Cost", "Date", "Employee ID"), show='headings')
        style = ttk.Style()
        style.configure("Treeview", rowheight=100)
        self.myfont = (tkfont.Font(**HEADER_FONT_PROPERTIES))
        style.configure("Treeview.Heading",
                        font=(self.myfont))

        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Cost", text="Cost", anchor=tk.CENTER)
        self.tree.heading("Date", text="Date", anchor=tk.CENTER)
        self.tree.heading("Employee ID", text="Employee", anchor=tk.CENTER)

        self.tree.column("ID", anchor=tk.CENTER)
        self.tree.column("Cost", anchor=tk.CENTER)
        self.tree.column("Date", anchor=tk.CENTER)
        self.tree.column("Employee ID", anchor=tk.CENTER)

        # Create vertical and horizontal scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Pack the Treeview and scrollbars
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Define tags for row colors
        self.tree.tag_configure("even_row", background="gray80")
        self.tree.tag_configure("odd_row", background="gray90")

        # Define tag for row font style
        self.tree.tag_configure("row_tag", font=tkfont.Font(**ROW_FONT_PROPERTIES))

        # Load images and insert data into the Treeview
        self._populate_treeview()

        self.tree.bind_all("<MouseWheel>", self._on_mousewheel)
        self.tree.bind('<<TreeviewSelect>>', self._on_item_selected)

    def _populate_treeview(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self._data = database.model.order.Order.get_all()
        except Exception as e:
            print(f"Database Error: {e}")
            self._data = []

        # Print status
        if not self._data:  # Check if the list is empty
            print("No menu items found.")
        else:
            print("Menu Items retrieved successfully:")

        # Insert data into the Treeview
        for i, item in enumerate(self._data):
            try:
                # Determine row tag based on index
                item_tag = "even_row" if i % 2 == 0 else "odd_row"

                # Insert item into the Treeview
                item_id = self.tree.insert("", "end", values=(
                    item.id,
                    f"$ {item.cost}",
                    item.date,
                    item.employee_id
                ))
                self.tree.item(item_id, tags=("row_tag", item_tag))

            except Exception as e:
                print(f"Data Error: {e}")
    """
    def _create_body_content_2(self,panel):
        # Add content to the body panel
        tk.Label(panel, text="Menu Items", font=tkfont.Font(**CUSTOM_FONT_PROPERTIES)).pack(pady=20)

        # Create a frame for the table
        self.table_frame2 = tk.Frame(panel)
        self.table_frame2.pack(expand=True, fill=tk.BOTH)

        try:
            self._data = database.model.menuitem.MenuItem.get_all()
        except Exception as e:
            print(f"Database Error: {e}")
            self._data = []

        # Print status
        if not self._data:  # Check if the list is empty
            print("No menu items found.")
        else:
            print("Menu Items retrieved successfully:")

        # Create a Treeview widget
        self.tree2 = ttk.Treeview(self.table_frame2, columns=("ID", "Name", "Price", "Description", "Image"))
        style2 = ttk.Style()
        style2.configure("Treeview", rowheight=150)
        self.myfont = (tkfont.Font(**HEADER_FONT_PROPERTIES))
        style2.configure("Treeview.Heading",
                        font=(self.myfont))

        self.tree2.heading("#0", text="Image", anchor=tk.CENTER)
        self.tree2.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree2.heading("Name", text="Name", anchor=tk.CENTER)
        self.tree2.heading("Price", text="Price", anchor=tk.CENTER)
        self.tree2.heading("Description", text="Description", anchor=tk.CENTER)
        self.tree2.heading("Image", text="Image")

        self.tree2.column("#0", width=250, anchor=tk.CENTER)
        self.tree2.column("ID", anchor=tk.CENTER)
        self.tree2.column("Name", anchor=tk.CENTER)
        self.tree2.column("Price", anchor=tk.CENTER)
        self.tree2.column("Description", anchor=tk.CENTER)
        self.tree2.column("Image", width=0, stretch=tk.NO)

        # Create vertical and horizontal scrollbars
        vsb = ttk.Scrollbar(self.table_frame2, orient="vertical", command=self.tree2.yview)
        hsb = ttk.Scrollbar(self.table_frame2, orient="horizontal", command=self.tree2.xview)
        self.tree2.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Pack the Treeview and scrollbars
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree2.pack(fill=tk.BOTH, expand=True)

        # List to keep references to PhotoImage objects
        self.photos = []

        # Define tags for row colors
        self.tree2.tag_configure("even_row", background="gray80")
        self.tree2.tag_configure("odd_row", background="gray90")

        # Define tag for row font style
        self.tree2.tag_configure("row_tag", font=tkfont.Font(**ROW_FONT_PROPERTIES))

        # Load images and insert data into the Treeview
        self._populate_treeview_2()

        self.tree2.bind_all("<MouseWheel>", self._on_mousewheel_2)
        #self.tree.bind('<<TreeviewSelect>>', self._on_item_selected)

    def _populate_treeview_2(self):
        # Clear existing items and images
        for item in self.tree2.get_children():
            self.tree2.delete(item)
        self.photos.clear()

        try:
            self._data = database.model.menuitem.MenuItem.get_all()
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
                image_path = MENUITEM_IMG_PATH + item.image if item.image else IMG_PATH

                # Use the load_image function to load and resize the image
                try:
                    photo = load_image(image_path, size=(240, 240))  # Adjust size as needed
                except FileNotFoundError:
                    # Fallback to default image if file not found
                    photo = load_image(IMG_PATH, size=(240, 240))

                self.photos.append(photo)  # Keep a reference to the image

                # Determine row tag based on index
                item_tag = "even_row" if i % 2 == 0 else "odd_row"

                # Insert item into the Treeview
                item_id = self.tree2.insert("", "end", text="", image=photo,
                                           values=(item.id, item.name, f"$ {item.price}", item.description, item.image))
                self.tree2.item(item_id, tags=("row_tag", item_tag))

            except Exception as e:
                print(f"Image Error: {e}")
    """
    def _on_mousewheel(self, event):
        try:
            self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception as e:
            print(f"Scroll Error: {e}")

    def _on_mousewheel_2(self, event):
        try:
            self.tree2.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception as e:
            print(f"Scroll Error: {e}")

    def _on_item_selected(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        # if selected_item:
        #     item = self.tree.item(selected_item[0])
        #     values = item['values']
        #
        #     self._selected_id = values[0]

            # Update the entry fields with the selected item values

    def destroy(self):
        # Destroy all widgets in the body panel
        for widget in self.body_panel.winfo_children():
            widget.destroy()
        self.body_panel.destroy()
        #
        # for widget in self.body_panel_2.winfo_children():
        #     widget.destroy()
        # self.body_panel_2.destroy()