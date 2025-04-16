from PIL import Image, ImageFilter
import tkinter as tk
from tkinter import filedialog
import math
import os

def read_number(message, error_message, from_val, to_val):
    while True:
        number = input(message)
        if number.isdigit() and from_val <= int(number) <= to_val:
            return int(number)
        else:
            print(error_message)

def select_an_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Choose an Image", 
        filetypes=[("Images", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if file_path:
        return Image.open(file_path), os.path.dirname(file_path)
    return None, None

def convert_to_grayscale(image):
    return image.convert('L')

def is_grayscale(image):
    return image.mode == 'L'

def apply_smoothing(image):
    return image.filter(ImageFilter.GaussianBlur(radius=1))

def apply_sobel_operator(image):
    Kx = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]
    
    Ky = [
        [ 1,  2,  1],
        [ 0,  0,  0],
        [-1, -2, -1]
    ]
    
    width, height = image.size
    input_pixels = image.load()
    output_image = Image.new('L', (width, height))
    output_pixels = output_image.load()

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            gx = 0
            gy = 0
            for j in range(-1, 2):
                for i in range(-1, 2):
                    pixel = input_pixels[x + i, y + j]
                    gx += pixel * Kx[j + 1][i + 1]
                    gy += pixel * Ky[j + 1][i + 1]
            magnitude = int(math.sqrt(gx ** 2 + gy ** 2))
            output_pixels[x, y] = min(magnitude, 255)

    return output_image

def apply_threshold(image, threshold):
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            pixels[x, y] = 255 if pixels[x, y] >= threshold else 0
    return image

def process_image_versions(image, save_dir):
    if not is_grayscale(image):
        image = convert_to_grayscale(image)

    threshold = read_number("Enter edge threshold (0-255): ", "Invalid value. Please enter a value between 0 and 255.", 0, 255)

    sobel_raw = apply_sobel_operator(image.copy())
    thresholded_raw = apply_threshold(sobel_raw, threshold)
    raw_path = os.path.join(save_dir, "Edges_Without_Smoothing.png")
    thresholded_raw.save(raw_path)
    print(f"✅ Saved without smoothing: {raw_path}")

    smoothed = apply_smoothing(image.copy())
    sobel_smooth = apply_sobel_operator(smoothed)
    thresholded_smooth = apply_threshold(sobel_smooth, threshold)
    smooth_path = os.path.join(save_dir, "Edges_With_Smoothing.png")
    thresholded_smooth.save(smooth_path)
    print(f"✅ Saved with smoothing: {smooth_path}")

    thresholded_raw.show()
    thresholded_smooth.show()

def main():
    image, _ = select_an_image()
    
    if image:
        save_dir = os.path.dirname(os.path.realpath(__file__))
        process_image_versions(image, save_dir)
    else:
        print("⚠️ No image was selected.")

main()
