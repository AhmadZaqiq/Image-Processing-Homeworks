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
