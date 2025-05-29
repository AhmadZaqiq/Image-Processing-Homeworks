# **Image-Processing-Homeworks**

## **Thresholded Image Processor**
This code provides an image processing tool that allows the user to select an image, convert it to grayscale if necessary, and apply a threshold filter to isolate pixel values within a specified range. The user is prompted to enter a lower and upper threshold (between 0 and 255) for pixel values. The code then modifies the image by turning any pixels outside the specified range to black (0). The processed image is displayed and saved.

## **Sobel Edge Detection Processor**
This program performs edge detection on grayscale images using the Sobel operator. It allows the user to select an image, converts it to grayscale if needed, and automatically applies two types of edge detection:
- Direct Sobel edge detection.
- Smoothed edge detection (image is blurred before applying Sobel).

In both cases, a thresholding step is applied to isolate significant edges based on gradient magnitude. The two output images are displayed and saved automatically in the same directory as the Python script.

## **FieldMasker**
**FieldMasker** is an image processing tool that allows the user to select a football field image and automatically highlights green areas (typically grass) using a red transparent mask. The program detects pixels where the green color significantly exceeds the red and blue components, identifying them as "green areas". These areas are then overlaid with a semi-transparent red mask to make them visually stand out. The processed image is displayed and saved in the same directory as the script.

## **Cartoon Video Stylizer**

**Cartoon Video Stylizer** is a video processing tool that transforms any input video into a cartoon-like stylized output. The program allows the user to:

* Choose the number of colors for color quantization (between 8 and 512).
* Specify the thickness of black contours for edge emphasis (between 1 and 10).

The effect is achieved through several steps:

1. **Color Quantization**: Reduces the number of colors in each frame using uniform quantization, giving a simplified, artistic look.
2. **Blending**: Blends the quantized image with white to simulate a watercolor effect.
3. **Edge Detection**: Applies Canny edge detection followed by dilation to extract bold edges.
4. **Contour Application**: Overlays black edges on the color-simplified image to complete the cartoon effect.

The user is prompted to select an input video file and choose a path to save the output. The resulting video is automatically saved with the applied cartoon filter.

### **Required Libraries**

This program uses the following Python libraries:

* `cv2` (OpenCV) – for image and video processing.
* `numpy` – for numerical operations and array handling.
* `tkinter` – for graphical file selection dialogs.

## **Morphological Image Cleaner**

**Morphological Image Cleaner** is an image processing tool that allows the user to select an image, convert it to grayscale, and apply thresholding to isolate key features from the background based on a specified threshold value. It then uses advanced morphological operations (opening and closing) to remove noise and fill small holes inside objects.

The main steps include:

1. **Thresholding**: Convert the grayscale image into a binary image where pixels above the threshold become black (0) and those below become white (255).
2. **Morphological Opening**: Remove small noise by applying erosion followed by dilation.
3. **Morphological Closing**: Fill small holes inside objects by applying dilation followed by erosion.
4. **Restoration**: Reconstruct the original image over a white background, highlighting only the processed objects.

All intermediate and final images are displayed. The program also allows the user to select a file path to save the processed image.

### **Required Libraries**

* `cv2` (OpenCV) – for image processing and morphological operations.
* `numpy` – for numerical operations and array handling.
* `tkinter` – for graphical file dialogs for selecting and saving files.
