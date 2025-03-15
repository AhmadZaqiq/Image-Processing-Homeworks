from PIL import Image
import tkinter as tk
from tkinter import filedialog

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
        return Image.open(file_path)
    return None

def convert_to_grayscale(image):
    return image.convert('L')

def is_grayscale(image):
    return image.mode == 'L'

def apply_thresholds(image, lower_threshold, upper_threshold):
    pixels = image.load()
    width, height = image.size

    for i in range(width):
        for j in range(height):
            pixel_value = pixels[i, j]
            if lower_threshold <= pixel_value <= upper_threshold:
                continue
            pixels[i, j] = 0

    return image

def process_image(image):
    if not is_grayscale(image):
        image = convert_to_grayscale(image)
    
    lower_threshold = read_number("Enter lower threshold (0-255): ", "Invalid value. Please enter a value between 0 and 255.", 0, 255)
    upper_threshold = read_number("Enter upper threshold (0-255): ", "Invalid value. Please enter a value between 0 and 255.", 0, 255)
    
    thresholded_image = apply_thresholds(image, lower_threshold, upper_threshold)
    thresholded_image.show()
    
    return thresholded_image

def save_image(image):
    save_path = filedialog.asksaveasfilename(
        title="Save Image", 
        defaultextension=".png", 
         initialfile="Thresholded_Image.png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpeg;*.jpg"), ("All files", "*.*")]
    )
    
    if save_path:
        image.save(save_path)
        print("✅ Image saved successfully!")

def main():
    image = select_an_image()
    
    if image:
        processed_image = process_image(image)
        save_image(processed_image)
    else:
        print("⚠️ No image was selected.")

main()
