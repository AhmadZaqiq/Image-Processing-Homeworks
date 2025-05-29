import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

# ============================
# Thresholding
# ============================
def apply_threshold(gray_image, threshold_value=240):
    """Apply binary inverse threshold using NumPy vectorized logic."""
    return np.where(gray_image > threshold_value, 0, 255).astype(np.uint8)

# ============================
# Morphological Operations
# ============================
def apply_opening_multiple(img, kernel, iterations):
    """Apply morphological opening (erosion followed by dilation)."""
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)

def apply_closing_multiple(img, kernel, iterations):
    """Apply morphological closing (dilation followed by erosion)."""
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)

# ============================
# Restore original colors
# ============================
def restore_image(original, mask):
    """Keep original colors where mask is white, background is white."""
    restored = np.full_like(original, 255)
    restored[mask] = original[mask]
    return restored

# ============================
# File dialogs
# ============================
def select_image_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    root.destroy()
    return file_path

def save_image_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="Save Processed Image",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

# ============================
# Main Function
# ============================
def main():
    input_path = select_image_file()
    if not input_path:
        print("⚠️ No image selected!")
        return

    image = cv2.imread(input_path)
    if image is None:
        print("❌ Error: Unable to load the image.")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 1: Threshold
    threshold_value = 240
    thresh = apply_threshold(gray_image, threshold_value)

    # Step 2: Morphological Opening (remove noise)
    kernel_open = np.ones((5, 5), dtype=np.uint8)
    opened = apply_opening_multiple(thresh, kernel_open, iterations=2)

    # Step 3: Morphological Closing (fill holes)
    kernel_close = np.ones((11, 11), dtype=np.uint8)
    closed = apply_closing_multiple(opened, kernel_close, iterations=5)

    # Step 4: Restore original image over white background
    mask = closed == 255
    restored = restore_image(image, mask)

    # Show images
    cv2.imshow("Original Image", image)
    cv2.imshow("Grayscale Image", gray_image)
    cv2.imshow("Threshold Image", thresh)
    cv2.imshow("After Opening (Noise Removed)", opened)
    cv2.imshow("After Closing (Holes Filled)", closed)
    cv2.imshow("Restored Image with White Background", restored)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Ask to save the restored image
    save_path = save_image_file()
    if save_path:
        cv2.imwrite(save_path, restored)
        print(f"✅ Image saved at: {save_path}")
    else:
        print("⚠️ Image not saved.")

if __name__ == "__main__":
    main()
