import shutil
import uuid
import base64
import os


def _generate_uuid():
    """Generate a random UUID and encode it in base64."""
    random_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip("=")
    return random_uuid


def _get_new_file_name(selected_image_path):
    """Generate a new file name based on a UUID and the original file extension."""
    _, file_extension = os.path.splitext(selected_image_path)
    new_file_name = f"{_generate_uuid()}{file_extension}"
    return new_file_name


def save_image(selected_image_path, destination_dir):
    """Save the selected image to the specified directory with a new UUID-based file name."""
    if not selected_image_path:
        raise ValueError("No image selected to save.")

    new_file_name = _get_new_file_name(selected_image_path)
    destination_path = os.path.join(destination_dir, new_file_name)

    try:
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Copy the image to the new destination with the new name
        shutil.copy(selected_image_path, destination_path)
        return new_file_name
    except Exception as e:
        print(f"Error saving image: {e}")
        return None


def delete_image(image_file_name, destination_dir):
    """Delete the specified image file from the destination directory."""
    if not image_file_name:
        raise ValueError("No image file name provided for deletion.")

    # Construct the full path to the image file
    image_path = os.path.join(destination_dir, image_file_name)

    try:
        # Check if the file exists before attempting to delete it
        if os.path.isfile(image_path):
            os.remove(image_path)
            print(f"Image file {image_file_name} deleted successfully.")
        else:
            print(f"Image file {image_file_name} does not exist.")

    except Exception as e:
        print(f"Error deleting image file: {e}")

