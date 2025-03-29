import pytesseract
import cv2
from difflib import SequenceMatcher

# Function to calculate accuracy
def calculate_accuracy(ground_truth, recognized_text):
    matcher = SequenceMatcher(None, ground_truth, recognized_text)
    return matcher.ratio() * 100

# Load the image from which to extract text
image_path = 'path_to_your_image.png'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Resize the image to a larger size
resized_image = cv2.resize(gray_image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

# Apply thresholding to get a binary image
_, binary_image = cv2.threshold(resized_image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Remove noise using morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
cleaned_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

# Perform OCR on the cleaned image
recognized_text = pytesseract.image_to_string(cleaned_image)

# Define the ground truth text
ground_truth = "C:\Users\Devil\Desktop\bago"

# Calculate the OCR accuracy
accuracy = calculate_accuracy(ground_truth, recognized_text)

print(f"Recognized Text: {recognized_text}")
print(f"Ground Truth Text: {ground_truth}")
print(f"OCR Accuracy: {accuracy:.2f}%")

import cv2
import pytesseract

# Path to Tesseract executable (update this for your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove noise using Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding
    _, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Resize image (optional, for better OCR accuracy)
    resized = cv2.resize(thresholded, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    return resized

def perform_ocr(image_path):
    # Preprocess the image
    processed_image = preprocess_image(image_path)

    # Run OCR on the preprocessed image
    text = pytesseract.image_to_string(processed_image)

    return text

# Test the OCR enhancement
if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"  # Replace with your image file
    extracted_text = perform_ocr(image_path)
    print("Extracted Text:")
    print(extracted_text)
