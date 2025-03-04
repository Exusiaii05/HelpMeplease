import cv2
import pytesseract
import requests
from gensim.summarization import summarize
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  # Update this path based on your installation

API_ENDPOINT = "https://your-api-endpoint.com/summarize"  # Update this with your actual API endpoint

class TextScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Scanner and Summarizer")
        self.geometry("800x600")

        self.camera_label = ttk.Label(self, text="Camera Preview")
        self.camera_label.pack()

        self.capture_button = ttk.Button(self, text="Capture Image", command=self.capture_image)
        self.capture_button.pack()

        self.recognized_text_label = ttk.Label(self, text="Recognized Text:")
        self.recognized_text_label.pack()
        self.recognized_text = tk.Text(self, height=10, width=80)
        self.recognized_text.pack()

        self.summary_label = ttk.Label(self, text="Summary:")
        self.summary_label.pack()
        self.summary_text = tk.Text(self, height=10, width=80)
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
            gray = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            self.recognized_text.delete(1.0, tk.END)
            self.recognized_text.insert(tk.END, text)
            summary = self.get_summary_from_api(text)
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, summary)
        else:
            messagebox.showerror("Error", "Failed to capture image from camera.")

    def get_summary_from_api(self, text):
        try:
            response = requests.post(API_ENDPOINT, json={"text": text})
            response.raise_for_status()
            summary = response.json().get("summary", "No summary available.")
        except requests.RequestException as e:
            summary = f"API request failed: {e}"
        return summary

    def on_closing(self):
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = TextScannerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()