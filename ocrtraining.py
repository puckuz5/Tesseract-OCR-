import cv2

# Correct the file path for your image
img = cv2.imread(r'C:\Users\ketan\OneDrive\Desktop\imagetotext\mywriting.jpg', cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Error: Image not found.")
else:
    # Convert to binary image using thresholding
    _, binary_image = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)

    # Save the processed image using a valid path
    cv2.imwrite(r'C:\Users\ketan\OneDrive\Desktop\imagetotext\processed_mywriting.jpg', binary_image)

