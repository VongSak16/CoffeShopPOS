from tkinter import filedialog

from utils.load_image import load_image


def open_image_dialog(image_label, image):
    """Open an image dialog and update the image label with the selected image."""
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )

    # Initialize photo to None
    photo = None

    if file_path:
        photo = load_image(file_path, size=(400, 400))  # Adjust size as needed
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to the image
        # print(f"Selected image path: {file_path}")

    return file_path, photo
