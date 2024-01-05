import os
from PIL import Image
from tqdm import tqdm
import time


def resize_and_compress_images(
    original_folder_path, resized_folder_path, new_width, new_height
):
    # Create the resized folder if it doesn't exist
    os.makedirs(resized_folder_path, exist_ok=True)

    # Get the total number of images for the progress bar
    total_images = len(
        [
            filename
            for filename in os.listdir(original_folder_path)
            if filename.lower().endswith((".jpg", ".jpeg"))
        ]
    )

    # Initialize the progress bar
    progress_bar = tqdm(total=total_images, desc="Processing Images")

    # Loop through all images in the original folder
    for filename in os.listdir(original_folder_path):
        # Skip files that are not images
        if not filename.lower().endswith((".jpg", ".jpeg")):
            continue

        # Build the full file paths
        original_path = os.path.join(original_folder_path, filename)
        resized_path = os.path.join(resized_folder_path, filename)

        # Open the image
        with Image.open(original_path) as img:
            # Check if the image is smaller than the new dimensions
            if img.width <= new_width and img.height <= new_height:
                # Convert the image to RGB format
                img = img.convert("RGB")

                # Save the image with a compressed format
                img.save(resized_path, quality=50, optimize=True)
                progress_bar.update(1)
                continue

            # Calculate the new dimensions while maintaining the aspect ratio
            aspect_ratio = img.width / img.height
            new_dimensions = (new_width, int(new_width / aspect_ratio))
            if new_dimensions[1] > new_height:
                new_dimensions = (int(new_height * aspect_ratio), new_height)

            # Resize the image to the new dimensions
            img = img.resize(new_dimensions, Image.LANCZOS)

            # Check if the new image is smaller than the new dimensions
            if img.width < new_width and img.height < new_height:
                # Save the original image without resizing
                img = img.convert("RGB")
                img.save(resized_path, quality=50, optimize=True)
                progress_bar.update(1)
                continue

            # Convert the image to RGB format
            img = img.convert("RGB")

            # Save the resized image with a compressed format
            img.save(resized_path, quality=85, optimize=True)
            progress_bar.update(1)

    progress_bar.close()
    print("All images in the folder have been resized and compressed.")


# Timer function to measure execution time
def run_with_timer(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")


# Set the paths and dimensions
original_folder_path = "/users/usr/desktop/folder-name"
resized_folder_path = "/users/usr/desktop/folder-name-resized"
new_width = 2500
new_height = 2500

# Call the function with the specified parameters using the timer
run_with_timer(
    resize_and_compress_images,
    original_folder_path,
    resized_folder_path,
    new_width,
    new_height,
)
