import os
from PIL import Image
import numpy as np

DIRECTORY = "assets/pizzas"
SIZE = 1024
DPI = 96

def process_image(image_path, size=SIZE, dpi=DPI, overwrite=False):
    """
    Processes an image by resizing it to the specified size and setting the specified DPI.
    Args:
        image_path (str): The path to the image file to be processed.
        size (int, optional): The target size for the image's width and height. Defaults to SIZE.
        dpi (int, optional): The target DPI (dots per inch) for the image. Defaults to DPI.
        overwrite (bool, optional): Whether to overwrite the original image file. If False, 
                                    the processed image will be saved with "_resized" appended 
                                    to the file name. Defaults to False.
    Returns:
        None
    """
    img = Image.open(image_path)
    img = img.convert("RGBA")  # Ensure consistent format

    # Crop the image to remove transparent edges
    img_array = np.array(img)   # convert to numpy array
    alpha = img_array[:, :, -1]  # extract the alpha channel
    # Find the bounding box of non-empty content
    rows = np.any(alpha != 0, axis=1)
    cols = np.any(alpha != 0, axis=0)
    first_row, last_row = np.where(rows)[0][[0, -1]]
    first_col, last_col = np.where(cols)[0][[0, -1]]
    # Crop the image
    img = img.crop((first_col, first_row, last_col + 1, last_row + 1))

    # Check if the image is already of proper size and resolution
    if img.size == (size, size) and img.info.get("dpi") == (dpi, dpi):
        print(f"Skipping {image_path} as it is already correct size and DPI")
        return False

    # Resize while maintaining aspect ratio
    img_proc = img.resize((size, size), Image.LANCZOS)

    if not overwrite:
        # Append "_processed" to the file name
        image_path = image_path.replace(".", "_processed.")

    # Save with correct DPI
    img_proc.save(image_path, dpi=(dpi, dpi))
    print(f"Processed {image_path}")
    return True

if __name__ == "__main__":
    for filename in os.listdir(DIRECTORY):
        if filename.lower().endswith(".png"):
            path = os.path.join(DIRECTORY, filename)
            process_image(path, overwrite=True)

    print("Processing complete.")
    

