from PIL import Image, ImageTk

def load_image(path, size=None):
    """Load and optionally resize an image with aspect ratio preserved (fill mode)."""
    image = Image.open(path)

    if size:
        # Calculate the aspect ratio of the image and the target size
        original_aspect = image.width / image.height
        target_aspect = size[0] / size[1]

        if original_aspect > target_aspect:
            # Image is wider than the target size, crop the sides
            new_width = int(target_aspect * image.height)
            crop_box = (
                (image.width - new_width) // 2,  # left
                0,  # top
                (image.width + new_width) // 2,  # right
                image.height  # bottom
            )
        else:
            # Image is taller than the target size, crop the top and bottom
            new_height = int(image.width / target_aspect)
            crop_box = (
                0,  # left
                (image.height - new_height) // 2,  # top
                image.width,  # right
                (image.height + new_height) // 2  # bottom
            )

        # Crop and resize the image
        image = image.crop(crop_box).resize(size, Image.LANCZOS)

    return ImageTk.PhotoImage(image)
