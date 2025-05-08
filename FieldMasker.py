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

def is_green_pixel(hue, saturation, value):
    return (hue >= 60 and hue <= 150) and (saturation > 0.4 and value > 0.3)

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val
    
    if delta == 0:
        hue = 0
    elif max_val == r:
        hue = (60 * ((g - b) / delta) + 360) % 360
    elif max_val == g:
        hue = (60 * ((b - r) / delta) + 120) % 360
    else:
        hue = (60 * ((r - g) / delta) + 240) % 360
    
    if max_val == 0:
        saturation = 0
    else:
        saturation = delta / max_val
    
    value = max_val
    
    return hue, saturation, value

def detect_green_pixels(image):
    width, height = image.size
    input_pixels = image.load()

    red_mask = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    mask_pixels = red_mask.load()

    for y in range(height):
        for x in range(width):
            r, g, b = input_pixels[x, y]
            hue, saturation, value = rgb_to_hsv(r, g, b)
            if is_green_pixel(hue, saturation, value):
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
