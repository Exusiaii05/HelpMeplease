import cv2
import pytesseract
import numpy as np

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_image():
    """Captures an image from the webcam and returns it."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    print("Press 's' to capture an image or 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow('Camera', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):  # Capture image when 's' is pressed
            image = frame.copy()
            break
        elif key == ord('q'):  # Quit if 'q' is pressed
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()
    return image

def preprocess_image(image):
    """Preprocess image for better OCR accuracy."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    gray = cv2.medianBlur(gray, 3)  # Reduce noise (better for OCR)

    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 11, 2)

    scale_percent = 200  # Scale by 200%
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_CUBIC)

    kernel = np.ones((1, 1), np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    
    return gray

def recognize_text(image):
    """Extract text using Tesseract OCR with optimized settings."""
    processed_image = preprocess_image(image)

    custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'

    text = pytesseract.image_to_string(processed_image, config=custom_config)
    return text.strip()

def main():
    """Main function to capture and process an image."""
    image = capture_image()
    if image is None:
        print("No image captured. Exiting.")
        return

    text = recognize_text(image)
    if not text.strip():
        print("No text recognized. Exiting.")
        return

    print("\n📜 Recognized Text:\n", text)

if __name__ == "__main__":
    main()
