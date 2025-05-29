import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def read_number(message, error_message, from_val, to_val):
    while True:
        number = input(message)
        if number.isdigit() and from_val <= int(number) <= to_val:
            return int(number)
        else:
            print(error_message)

def select_video_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")]
    )
    root.destroy()
    return file_path

def save_video_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="Save Output Video",
        defaultextension=".mp4",
        initialfile="Result",
        filetypes=[("MP4 files", "*.mp4"), ("AVI files", "*.avi"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

def quantize_colors(image, n_colors):
    """Reduce color palette using uniform quantization"""
    n_bins = max(1, min(8, round(n_colors ** (1/3))))  # Limit to 8 bins per channel
    step = 256 / n_bins
    table = np.array([min(n_bins-1, i//step) * step + step/2 for i in range(256)])
    return table[image].astype(np.uint8)

def process_frame(frame, n_colors, edge_thickness):
    """Apply cartoon effect to a single frame"""
    # Step 1: Reduce colors
    quantized = quantize_colors(frame, n_colors)
    
    # Step 2: Lighten colors (simulate watercolor on white background)
    alpha = 0.7  # Blend factor with white
    white = np.full_like(quantized, 255)
    blended = cv2.addWeighted(quantized, alpha, white, 1 - alpha, 0)
    
    # Step 3: Edge detection and processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    kernel = np.ones((edge_thickness, edge_thickness), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel)
    
    # Step 4: Apply black contours
    result = blended.copy()
    result[dilated_edges > 0] = 0  # Set edges to black
    
    return result

def get_user_parameters():
    """Prompt user for number of colors and edge thickness."""
    n_colors = read_number(
        "Enter number of colors (8-512): ",
        "Invalid input. Please enter a number between 8 and 512.",
        8, 512
    )
    edge_thickness = read_number(
        "Enter edge thickness (1-10): ",
        "Invalid input. Please enter a number between 1 and 10.",
        1, 10
    )
    return n_colors, edge_thickness

def get_video_paths():
    """Handle file selection dialogs for input and output paths."""
    input_path = select_video_file()
    if not input_path:
        print("⚠️ No input video selected!")
        return None, None

    output_path = save_video_file()
    if not output_path:
        print("⚠️ No output path selected!")
        return None, None

    return input_path, output_path

def setup_video_io(input_path, output_path):
    """Open input video and prepare output writer."""
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("❌ Error opening video file!")
        return None, None, None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        print("❌ Error creating output video!")
        cap.release()
        return None, None, None

    return cap, out, fps

def process_video(cap, out, n_colors, edge_thickness):
    """Apply cartoon effect to all frames in the video."""
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = process_frame(frame, n_colors, edge_thickness)
        out.write(processed_frame)
        frame_count += 1

        if frame_count % 30 == 0:
            print(f"⏳ Processed {frame_count} frames...")

    print(f"✅ Processing complete! Saved {frame_count} frames.")

def main():
    n_colors, edge_thickness = get_user_parameters()
    input_path, output_path = get_video_paths()

    if not input_path or not output_path:
        return

    cap, out, _ = setup_video_io(input_path, output_path)
    if not cap or not out:
        return

    process_video(cap, out, n_colors, edge_thickness)

    cap.release()
    out.release()

if __name__ == "__main__":
    main()
