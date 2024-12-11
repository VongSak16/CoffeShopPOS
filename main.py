import tkinter as tk

from gui.login_frame import LoginFrame
from gui.main_layout import MainLayout


def on_login_success(user):
    # This function is called when the login is successful
    # You can now switch to the main layout of your application
    login_frame.pack_forget()  # Hide the login frame
    app = MainLayout(root, user)     # Initialize the main layout

def main():
    global root, login_frame
    root = tk.Tk()
    root.title("My Application")

    # # Initialize the login frame and display it
    login_frame = LoginFrame(root, on_login_success)
    login_frame.pack(fill='both', expand=True)

    # root = tk.Tk()
    # root.title("My Application")
    # app = MainLayout(root)
    root.mainloop()

if __name__ == "__main__":
    main()
