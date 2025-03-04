import cv2
import pytesseract
from gensim.summarization import summarize
import numpy as np

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  # Update this path based on your installation

def capture_image():
    # Initialize the camera
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
        if key == ord('s'):
            image = frame.copy()
            break
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()
    return image

def recognize_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def summarize_text(text):
    try:
        summary = summarize(text)
    except ValueError:
        summary = "Text is too short to summarize."
    return summary

def main():
    image = capture_image()
    if image is None:
        print("No image captured. Exiting.")
        return

    text = recognize_text(image)
    if not text.strip():
        print("No text recognized. Exiting.")
        return
    print("Recognized Text:\n", text)

    summary = summarize_text(text)
    print("\nSummary:\n", summary)

if __name__ == "__main__":
    main()