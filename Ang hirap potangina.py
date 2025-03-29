import cv2
import pytesseract
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from spellchecker import SpellChecker
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Set the path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TextScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Scanner and Summarizer")
        self.geometry("800x600")

        # UI Elements
        self.camera_label = ttk.Label(self, text="Camera Preview")
        self.camera_label.pack()

        self.capture_button = ttk.Button(self, text="Capture Image", command=self.capture_image)
        self.capture_button.pack()

        self.recognized_text_label = ttk.Label(self, text="Recognized Text:")
        self.recognized_text_label.pack()
        self.recognized_text = tk.Text(self, height=10, width=80, font=("Arial", 12), wrap="word")
        self.recognized_text.pack()

        self.summary_label = ttk.Label(self, text="Summary:")
        self.summary_label.pack()
        self.summary_text = tk.Text(self, height=10, width=80, font=("Arial", 12), wrap="word")
        self.summary_text.pack()

        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        self.after(10, self.update_camera)

    def capture_image(self):
        if hasattr(self, 'current_frame'):
            processed_image = self.preprocess_image(self.current_frame)
            text = self.extract_text(processed_image)
            text = self.correct_spelling(text)  # <<<< This function is missing! Add it below!

            self.recognized_text.delete(1.0, tk.END)
            self.recognized_text.insert(tk.END, text)

            summary = self.summarize_text(text)
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, summary)
        else:
            messagebox.showerror("Error", "Failed to capture image from camera.")

    def preprocess_image(self, image):
        """ Apply preprocessing for better OCR accuracy """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)  # Improve contrast

        # Resize for better text clarity
        scale_percent = 150  # Scale by 150%
        width = int(gray.shape[1] * scale_percent / 100)
        height = int(gray.shape[0] * scale_percent / 100)
        gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_CUBIC)

        return gray

    def extract_text(self, image):
        """ Extract text using Tesseract OCR with optimized settings """
        custom_config = r'--oem 3 --psm 6'  # LSTM OCR Engine, Assume Block of Text
        text = pytesseract.image_to_string(image, config=custom_config)
        return text.strip()

    def correct_spelling(self, text):
        """Fix spelling errors in OCR-extracted text"""
        spell = SpellChecker()
        words = text.split()
        corrected_words = [spell.correction(word) if spell.correction(word) else word for word in words]
        return " ".join(corrected_words)

    def summarize_text(self, text, sentence_count=3):
        """ Summarize text using Sumy LSA Summarizer """
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, sentence_count)
            return " ".join(str(sentence) for sentence in summary)
        except ValueError:
            return "Text is too short to summarize."

    def on_closing(self):
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = TextScannerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

import threading

def real_time_recognition(self):
    """Perform real-time OCR on the live camera feed."""
    if not hasattr(self, 'real_time_active'):
        self.real_time_active = False

    if not self.real_time_active:
        self.real_time_active = True
        self.recognized_text.delete(1.0, tk.END)
        threading.Thread(target=self.perform_real_time_ocr).start()
    else:
        self.real_time_active = False

def perform_real_time_ocr(self):
    """Continuously process frames for OCR while real-time mode is active."""
    while self.real_time_active:
        if hasattr(self, 'current_frame'):
            processed_image = self.preprocess_image(self.current_frame)
            text = self.extract_text(processed_image)
            text = self.correct_spelling(text)  # Optional for improved accuracy
            self.recognized_text.delete(1.0, tk.END)
            self.recognized_text.insert(tk.END, text)
        self.update()  # Refresh GUI


class TextScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.real_time_button = ttk.Button(self, text="Start Real-Time OCR", command=self.real_time_recognition)
        self.real_time_button.pack()

    def real_time_recognition(self):
        print("Real-Time OCR triggered!")  # Placeholder for testing


    from tkinter import ttk

class TextScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Scanner and Summarizer")
        self.geometry("800x600")

        # UI Elements
        self.camera_label = ttk.Label(self, text="Camera Preview")
        self.camera_label.pack()

        self.capture_button = ttk.Button(self, text="Capture Image", command=self.capture_image)
        self.capture_button.pack()

        self.recognized_text_label = ttk.Label(self, text="Recognized Text:")
        self.recognized_text_label.pack()
        self.recognized_text = tk.Text(self, height=10, width=80, font=("Arial", 12), wrap="word")
        self.recognized_text.pack()

        self.summary_label = ttk.Label(self, text="Summary:")
        self.summary_label.pack()
        self.summary_text = tk.Text(self, height=10, width=80, font=("Arial", 12), wrap="word")
        self.summary_text.pack()

        # Add Progress Bar widget
        self.progress_label = ttk.Label(self, text="OCR Progress:")
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()
        self.progress_bar["value"] = 0  # Initialize progress bar value

        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    # Additional methods here...


    from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Function for text summarization
def summarize_text(text, sentences_count=154):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return " ".join([str(sentence) for sentence in summary])

# Example usage
text = """
Artificial Intelligence (AI) is a branch of computer science that aims to create machines 
that can perform tasks that typically require human intelligence. It includes areas like 
machine learning, natural language processing, computer vision, and more.
"""
summary = summarize_text(text, sentences_count=2)
print("Summary:")
print(summary)
