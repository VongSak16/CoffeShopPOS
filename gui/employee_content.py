import tkinter as tk
from tkinter import ttk, messagebox
import database.model.employee
from utils.appearance import *
import tkinter.font as tkfont

from utils.load_image import load_image
from utils.open_image_dialog import open_image_dialog
import os

from utils.image_handle import save_image, delete_image

class EmployeeContent:

    def __init__(self, master):
        self._selected_id = None
        self._selected_image_path = ""
        self._image_path = "assets/employee/"

        self.master = master

        self.body_panel = tk.Frame(self.master, bg="red")
        self.body_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._create_body_content()

        self.right_nav_panel = tk.Frame(self.master, bg="lightgray", width=160)
        self.right_nav_panel.pack(side=tk.RIGHT, fill=tk.Y, anchor='nw')

        self._create_right_nav_content()

    def _create_body_content(self):
        # Add content to the body panel
        tk.Label(self.body_panel, text="Employees", font=tkfont.Font(**CUSTOM_FONT_PROPERTIES)).pack(pady=20)

        # Create a frame for the table
        self.table_frame = tk.Frame(self.body_panel)
        self.table_frame.pack(expand=True, fill=tk.BOTH)

        try:
            self._data = database.model.employee.Employee.get_all()
        except Exception as e:
            print(f"Database Error: {e}")
            self._data = []

        # Print status
        if not self._data:  # Check if the list is empty
            print("No employees found.")
        else:
            print("Employees retrieved successfully:")

        # Create a Treeview widget
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Name", "Role", "Phone", "Username", "Password", "Image"))
        style = ttk.Style()
        style.configure("Treeview", rowheight=250)
        self.myfont = (tkfont.Font(**HEADER_FONT_PROPERTIES))
        style.configure("Treeview.Heading",
                        font=(self.myfont))

        self.tree.heading("#0", text="Image", anchor=tk.CENTER)
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Name", text="Name", anchor=tk.CENTER)
        self.tree.heading("Role", text="Role", anchor=tk.CENTER)
        self.tree.heading("Phone", text="Phone", anchor=tk.CENTER)
        self.tree.heading("Username", text="Username", anchor=tk.CENTER)
        self.tree.heading("Password", text="Password", anchor=tk.CENTER)
        self.tree.heading("Image", text="Image")

        self.tree.column("#0", width=250, anchor=tk.CENTER)
        self.tree.column("ID", anchor=tk.CENTER)
        self.tree.column("Name", anchor=tk.CENTER)
        self.tree.column("Role", anchor=tk.CENTER)
        self.tree.column("Phone", anchor=tk.CENTER)
        self.tree.column("Username", anchor=tk.CENTER)
        self.tree.column("Password", width=0, stretch=tk.NO)
        self.tree.column("Image", width=0, stretch=tk.NO)

        # Create vertical and horizontal scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Pack the Treeview and scrollbars
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

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
            self._data = database.model.employee.Employee.get_all()
        except Exception as e:
            print(f"Database Error: {e}")
            self._data = []

        # Print status
        if not self._data:  # Check if the list is empty
            print("No employees found.")
        else:
            print("Employees retrieved successfully:")

        # Load images and insert data into the Treeview
        for i, item in enumerate(self._data):
            try:
                image_path = EMPLOYEE_IMG_PATH + item.image if item.image else IMG_PATH

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
                item_id = self.tree.insert("", "end", text="", image=photo,
                                           values=(item.id, item.name, item.role, item.phone, item.username, item.password, item.image))
                self.tree.item(item_id, tags=("row_tag", item_tag))

            except Exception as e:
                print(f"Image Error: {e}")

    def _create_right_nav_content(self):
        _PADY = 5
        _PADX = 10

        # Title label
        ttk.Label(self.right_nav_panel, text="Left Navigation",
                  font=font.Font(**CUSTOM_FONT_PROPERTIES),
                  foreground=LABEL_COLOR).grid(row=0, column=0, columnspan=2, pady=10)

        # Adding a label and input field for "Name"
        ttk.Label(self.right_nav_panel, text="Name:",
                  font=font.Font(**LABEL_FONT_PROPERTIES),
                  foreground=LABEL_COLOR).grid(row=1, column=0, pady=_PADY, padx=_PADX, sticky=tk.W)
        self.name_entry = tk.Entry(self.right_nav_panel,
                                   font=tkfont.Font(**ENTRY_FONT_PROPERTIES))
        self.name_entry.grid(row=1, column=1, pady=_PADY, padx=_PADX, sticky=tk.EW)

        # Adding a label and input field for "Role"
        ttk.Label(self.right_nav_panel, text="Role:",
                  font=font.Font(**LABEL_FONT_PROPERTIES),
                  foreground=LABEL_COLOR).grid(row=2, column=0, pady=_PADY, padx=_PADX, sticky=tk.W)
        self.role_entry = tk.Entry(self.right_nav_panel,
                                   font=tkfont.Font(**ENTRY_FONT_PROPERTIES))
        self.role_entry.grid(row=2, column=1, pady=_PADY, padx=_PADX, sticky=tk.EW)

        # Adding a label and input field for "Phone"
        ttk.Label(self.right_nav_panel, text="Phone:",
                  font=font.Font(**LABEL_FONT_PROPERTIES),
                  foreground=LABEL_COLOR).grid(row=3, column=0, pady=_PADY, padx=_PADX, sticky=tk.W)
        self.phone_entry = tk.Entry(self.right_nav_panel,
                                    font=tkfont.Font(**ENTRY_FONT_PROPERTIES))
        self.phone_entry.grid(row=3, column=1, pady=_PADY, padx=_PADX, sticky=tk.EW)

        # Adding a label and input field for "Username"
        ttk.Label(self.right_nav_panel, text="Username:",
                  font=font.Font(**LABEL_FONT_PROPERTIES),
                  foreground=LABEL_COLOR).grid(row=4, column=0, pady=_PADY, padx=_PADX, sticky=tk.W)
        self.username_entry = tk.Entry(self.right_nav_panel,
                                    font=tkfont.Font(**ENTRY_FONT_PROPERTIES))
        self.username_entry.grid(row=4, column=1, pady=_PADY, padx=_PADX, sticky=tk.EW)

        # Adding a label and input field for "Username"
        ttk.Label(self.right_nav_panel, text="Password:",
                  font=font.Font(**LABEL_FONT_PROPERTIES),
                  foreground=LABEL_COLOR).grid(row=5, column=0, pady=_PADY, padx=_PADX, sticky=tk.W)
        self.password_entry = tk.Entry(self.right_nav_panel, show='*',
                                       font=tkfont.Font(**ENTRY_FONT_PROPERTIES))
        self.password_entry.grid(row=5, column=1, pady=_PADY, padx=_PADX, sticky=tk.EW)

        # Adding a label and an image
        ttk.Label(self.right_nav_panel, text="Image:",
                  font=font.Font(**LABEL_FONT_PROPERTIES),
                  foreground=LABEL_COLOR).grid(row=6, column=0, pady=_PADY, padx=_PADX, sticky=tk.NW)
        # Load the image
        self.image = load_image("assets/img.png", size=(400, 400))  # Replace with your image path
        self.image_label = tk.Button(self.right_nav_panel, image=self.image, command=self._open_image_dialog)
        self.image_label.grid(row=6, column=1, pady=_PADY, padx=_PADX, sticky=tk.EW)

        self._create_crud_panel(_PADX, _PADY,7)

    def _open_image_dialog(self):
        """Open image dialog and update the image label."""
        file_path, photo = open_image_dialog(self.image_label, self.image)

        if file_path and photo:
            # If an image is selected, update the image reference and path
            self.image = photo
            self._selected_image_path = file_path
        else:
            # If no image is selected, revert to the default image
            self.image = load_image("assets/img.png", size=(400, 400))  # Replace with your default image path
            self._selected_image_path = ""  # Clear the selected image path

        # Update the image label with the current image
        self.image_label.config(image=self.image)
        print(self._selected_image_path)

    def _create_crud_panel(self, _PADX, _PADY, ROW):
        # Create a new frame for CRUD buttons
        self.right_nav_panel_bottom = tk.Frame(self.right_nav_panel, bg="white")
        self.right_nav_panel_bottom.grid(row=ROW, column=0, columnspan=2, pady=_PADY, padx=_PADX, sticky=tk.EW)
        # Configure columns to center-align
        self.right_nav_panel_bottom.columnconfigure(0, weight=1)
        self.right_nav_panel_bottom.columnconfigure(1, weight=1)
        self.right_nav_panel_bottom.columnconfigure(2, weight=1)
        # # CRUD BUTTONS
        self.create_button = tk.Button(self.right_nav_panel_bottom, text="Create",
                                       font=tkfont.Font(**ENTRY_FONT_PROPERTIES), bg="lightgreen",
                                       command=self._save_employee)
        self.create_button.grid(row=0, column=0, pady=_PADY, padx=_PADX, sticky=tk.EW)
        self.update_button = tk.Button(self.right_nav_panel_bottom, text="Update",
                                       font=tkfont.Font(**ENTRY_FONT_PROPERTIES), bg="lightblue",
                                       command=self._update_employee)
        self.update_button.grid(row=0, column=1, pady=_PADY, padx=_PADX, sticky=tk.EW)
        self.delete_button = tk.Button(self.right_nav_panel_bottom, text="Delete",
                                       font=tkfont.Font(**ENTRY_FONT_PROPERTIES), bg="salmon",
                                       command=self._delete_employee)
        self.delete_button.grid(row=0, column=2, pady=_PADY, padx=_PADX, sticky=tk.EW)

    def _on_item_selected(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item['values']

            self._selected_id = values[0]

            # Update the entry fields with the selected item values
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])  # Assuming 'Name' is at index 1

            self.role_entry.delete(0, tk.END)
            self.role_entry.insert(0, values[2])

            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, values[3])

            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, values[4])

            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, values[5])

            # Update the image label with the selected item's image
            image_path = EMPLOYEE_IMG_PATH + values[6] if values[6] else IMG_PATH
            try:
                photo = load_image(image_path, size=(400, 400))  # Adjust size as needed
                self._selected_image_path = image_path
                print("ada", self._selected_image_path)

            except FileNotFoundError:
                photo = load_image(IMG_PATH, size=(400, 400))
                self._selected_image_path = ""

            self.image_label.config(image=photo)
            self.image = photo  # Keep a reference to the image

    def _save_employee(self):
        # Get the data from entry fields
        name = self.name_entry.get()
        role = self.role_entry.get()
        phone = self.phone_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        image_filename = self._selected_image_path

        # Validate data before saving
        if not name or not role or not phone or not username or not password:
            #print("All fields are required.")
            messagebox.showerror("Error", "All fields are required.")
            return

        # Validate the image file
        if image_filename and image_filename != IMG_PATH:
            if not os.path.isfile(image_filename):
                print("Selected image file does not exist.")
                return

            # Optional: Validate image format (e.g., check extension)
            valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
            _, file_extension = os.path.splitext(image_filename)
            if file_extension.lower() not in valid_extensions:
                print("Invalid image format. Supported formats are: .png, .jpg, .jpeg, .gif")
                return

            image_filename = save_image(image_filename, self._image_path)
        else:
            print("No image selected.")
            image_filename = ""

        # Save to the database
        try:


            # Assuming `Employee` is your model
            new_item = database.model.employee.Employee(name=name,
                                                        role=role,
                                                        phone=phone,
                                                        username=username,
                                                        password=password,
                                                        image=image_filename)
            print(new_item)
            new_item.save()
            print("Employee created successfully.")

            # Clear the entry fields after saving
            self.name_entry.delete(0, tk.END)
            self.role_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            self._populate_treeview()

        except Exception as e:
            if image_filename and image_filename != IMG_PATH:
                delete_image(image_filename, self._image_path)
            print(f"Error saving employee: {e}")
            error_message = str(e)
            if "Duplicate entry" in error_message:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            else:
                messagebox.showerror("Error", f"An error occurred: {error_message}")

    def _delete_employee(self):
        id = self._selected_id

        # Check if the selected ID is valid
        if not id:
            print("No item selected.")
            return

        # Validate that the employee exists
        item_to_delete = database.model.employee.Employee.get_by_id(id)
        if not item_to_delete:
            print(f"Employee with ID {id} does not exist.")
            self._populate_treeview()
            return

        try:
            if item_to_delete.image is not None and item_to_delete.image != "":
                delete_image(item_to_delete.image, self._image_path)
                self.image = load_image(IMG_PATH, size=(400, 400))
                self.image_label.config(image=self.image)

            database.model.employee.Employee.delete(item_to_delete.id)

            print(f"Employee with ID {id} deleted successfully.")

            self._selected_image_path = ""
            # Refresh the Treeview
            self._populate_treeview()
        except Exception as e:
            print(f"Error while deleting employee: {e}")

    def _update_employee(self):
        id = self._selected_id

        # Check if the selected ID is valid
        if not id:
            print("No item selected.")
            return

        # Validate that the employee exists
        item_to_update = database.model.employee.Employee.get_by_id(id)
        if not item_to_update:
            print(f"Employee with ID {id} does not exist.")
            self._populate_treeview()
            return

        # Get the data from entry fields
        name = self.name_entry.get()
        role = self.role_entry.get()
        phone = self.phone_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        image_filename = self._selected_image_path

        # Validate data before saving
        if not name or not role or not phone or not username or not password:
            print("All fields are required.")
            return

        # Handle image update
        if image_filename and image_filename != IMG_PATH:
            if not os.path.isfile(image_filename):
                print("Selected image file does not exist.")
                return

            # Optional: Validate image format (e.g., check extension)
            valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
            _, file_extension = os.path.splitext(image_filename)
            if file_extension.lower() not in valid_extensions:
                print("Invalid image format. Supported formats are: .png, .jpg, .jpeg, .gif")
                return

            image_filename = save_image(image_filename, self._image_path)

            # Check if the new image is the same as the old image
            if item_to_update.image and item_to_update.image != image_filename:
                delete_image(item_to_update.image, self._image_path)

        else:
            # No new image selected; keep the old one
            image_filename = item_to_update.image

        try:
            # Update the item in the database
            item_to_update.name = name
            item_to_update.role = role
            item_to_update.phone = phone
            item_to_update.username = username
            item_to_update.password = password
            item_to_update.image = image_filename

            item_to_update.save()  # Save changes to the database

            print(f"Employee with ID {id} updated successfully.")

            # Clear the selected ID and entry fields
            self._selected_id = None
            self._selected_image_path = ""
            self.name_entry.delete(0, tk.END)
            self.role_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            # Refresh the Treeview
            self._populate_treeview()

        except Exception as e:
            print(f"Error while updating employee: {e}")

    def destroy(self):
        # Destroy all widgets in the body panel
        for widget in self.body_panel.winfo_children():
            widget.destroy()
        self.body_panel.destroy()

        # Destroy all widgets in the right nav panel
        for widget in self.right_nav_panel.winfo_children():
            widget.destroy()
        self.right_nav_panel.destroy()