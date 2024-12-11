import tkinter as tk
from tkinter import font, messagebox
from utils.appearance import *
from ctypes import windll
import tkinter.font as tkfont
from gui.menuitem_content import MenuItemContent
from gui.employee_content import EmployeeContent
from gui.report_content import ReportContent
from gui.order_content import OrderContent
from utils.load_image import load_image

windll.shcore.SetProcessDpiAwareness(1)


class MainLayout:
    def __init__(self, _master, user):
        self._user = user
        self._master = _master
        self._master.title("Main Layout")
        self._master.geometry("1000x800")
        self._master.state("zoomed")

        # Define custom fonts
        self.custom_font = font.Font(**CUSTOM_FONT_PROPERTIES)

        self.top_panel = tk.Frame(self._master, bg="lightblue", height=50)
        self.top_panel.pack(side=tk.TOP, fill=tk.X)

        self.create_top_content()

        self.left_nav_panel = tk.Frame(self._master, bg="lightgray", width=200)
        self.left_nav_panel.pack(side=tk.LEFT, fill=tk.Y, anchor='nw')

        self.menuitems_icon = load_image("assets/icons/icons8-kawaii-coffee-96.png", size=(96, 96))
        self.sale_icon = load_image("assets/icons/icons8-receipt-96.png", size=(96, 96))
        self.user_icon = load_image("assets/icons/icons8-user-96.png", size=(96, 96))
        self.report_icon = load_image("assets/icons/icons8-invoice-96.png", size=(96, 96))
        self._create_left_nav_content()

        self.body_content = OrderContent(self._master, self._user)
        self.active_button = self.sale_button.config(bg="darkgray", fg="white")
        self._show_sale_content()


    def create_top_content(self):
        tk.Label(self.top_panel, text=f"Welcome {self._user['name']}", font=tkfont.Font(**CUSTOM_FONT_PROPERTIES),
                  foreground=LABEL_COLOR).pack(
            pady=10)

    def _create_left_nav_content(self):
        _PADY = 5
        _PADX = 10
        self.sale_button = tk.Button(self.left_nav_panel, text="Sale",
                  font=font.Font(**NAVBUTTON_FONT_PROPERTIES),
                  fg=NAVBUTTON_COLOR,
                  bg=NAVBUTTON_BG_COLOR,
                  image=self.sale_icon,
                  compound=tk.TOP,
                  command=self._show_sale_content)
        self.sale_button.pack(pady=_PADY, padx=_PADX, fill=tk.X)

        self.menu_button = tk.Button(self.left_nav_panel, text="Menu Items",
                  font=font.Font(**NAVBUTTON_FONT_PROPERTIES),
                  fg=NAVBUTTON_COLOR,
                  bg=NAVBUTTON_BG_COLOR,
                  image=self.menuitems_icon,
                  compound=tk.TOP,
                  command=self._show_menu_content)
        self.menu_button.pack(pady=_PADY, padx=_PADX, fill=tk.X)

        self.report_button = tk.Button(self.left_nav_panel, text="Report Orders",
                  font=font.Font(**NAVBUTTON_FONT_PROPERTIES),
                  fg=NAVBUTTON_COLOR,
                  bg=NAVBUTTON_BG_COLOR,
                  image=self.report_icon,
                  compound=tk.TOP,
                  command=self._show_report_content)
        self.report_button.pack(pady=_PADY, padx=_PADX, fill=tk.X)

        self.employee_button = tk.Button(self.left_nav_panel, text="Employee",
                  font=font.Font(**NAVBUTTON_FONT_PROPERTIES),
                  fg=NAVBUTTON_COLOR,
                  bg=NAVBUTTON_BG_COLOR,
                  image=self.user_icon,
                  compound=tk.TOP,
                  command=self._show_employee_content)
        self.employee_button.pack(pady=_PADY, padx=_PADX, fill=tk.X)

    def _show_menu_content(self):
        self._change_body_content(MenuItemContent(self._master), self.menu_button)

    def _show_report_content(self):
        self._change_body_content(ReportContent(self._master), self.report_button)

    def _show_sale_content(self):
        self._change_body_content(OrderContent(self._master, self._user), self.sale_button)

    def _show_employee_content(self):
        self._change_body_content(EmployeeContent(self._master), self.employee_button)

    def _change_body_content(self, new_content, active_button):
        # Destroy existing body content
        self.body_content.destroy()

        # Update body content
        self.body_content = new_content

        # Update button colors
        if self.active_button:
            self.active_button.config(bg=NAVBUTTON_BG_COLOR, fg=NAVBUTTON_COLOR)

        active_button.config(bg="darkgray", fg="white")
        self.active_button = active_button

    def dummy_command(self):
        pass
