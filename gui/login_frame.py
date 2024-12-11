import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont

from utils.appearance import CUSTOM_FONT_PROPERTIES
from utils.authchecker import AuthChecker


class LoginFrame(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master.title("Login")
        self.master.geometry("1000x800")
        self.on_login_success = on_login_success
        self.master = master
        self._create_widgets()
        self._center_window()

    def _create_widgets(self):
        # Define a custom font
        custom_font = tkfont.Font(**CUSTOM_FONT_PROPERTIES)

        # Username Label
        tk.Label(self, text="Username:", font=custom_font).grid(row=0, column=0, sticky='e', padx=5, pady=5)

        # Username Entry
        self.username_entry = tk.Entry(self, font=custom_font)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Password Label
        tk.Label(self, text="Password:", font=custom_font).grid(row=1, column=0, sticky='e', padx=5, pady=5)

        # Password Entry
        self.password_entry = tk.Entry(self, show='*', font=custom_font)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Login Button
        tk.Button(self, text="Login", bg="blue", fg="white", command=self._attempt_login, font=custom_font).grid(row=2, column=0, columnspan=2,
                                                                                          pady=10)

    def _attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Validation Error", "Both username and password are required.")
            return

        user = AuthChecker.authenticate(username, password)
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def _center_window(self):
        # Calculate window size
        window_width = 570
        window_height = 230

        # Get the screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the position to center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window size and position
        self.master.geometry(f'{window_width}x{window_height}+{x}+{y}')