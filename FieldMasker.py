import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

def select_an_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Choose a Football Field Image",
        filetypes=[("Images", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if file_path:
        try:
            return Image.open(file_path).convert('RGB'), os.path.dirname(file_path)
        except Exception as e:
            print(f"⚠️ Error opening image: {e}")
            return None, None
    return None, None

def is_green_pixel(r, g, b):
    return g > 100 and g > r + 20 and g > b + 20

def detect_green_pixels(image):
    width, height = image.size
    input_pixels = image.getdata()

    red_mask = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    mask_pixels = red_mask.load()

    for y in range(height):
        for x in range(width):
            r, g, b = input_pixels[y * width + x]
            if is_green_pixel(r, g, b):
                mask_pixels[x, y] = (255, 0, 0, 100)

    return Image.alpha_composite(image.convert('RGBA'), red_mask)

def process_image(image, save_dir):
    result = detect_green_pixels(image)
    if result:
        save_path = os.path.join(save_dir, "Football_Field_With_Red_Mask.png")
        result.save(save_path)
        print(f"✅ Saved result image at: {save_path}")
        result.show()
    else:
        print("⚠️ Error in processing the image.")

def main():
    image, _ = select_an_image()
    if image:
        save_dir = os.path.dirname(os.path.realpath(__file__))
        process_image(image, save_dir)
    else:
        print("⚠️ No image was selected.")

if __name__ == "__main__":
    main()
