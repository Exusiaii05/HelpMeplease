import cv2
import pytesseract
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import string

# Configure Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def recognize_text_from_image(image_path):
    """Perform OCR on the given image and return extracted text."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("C:\Users\Devil\Desktop\bago")
    
    # Preprocessing the image for better OCR results
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Extract text using Tesseract
    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(gray, config=custom_config)
    return text

def summarize_text(text, max_sentences=3):
    """Summarize text using frequency-based scoring (NLTK)."""
    if not text.strip():
        return "No text provided for summarization."

    sentences = sent_tokenize(text)

    # If text is too short, return it as is
    if len(sentences) <= max_sentences:
        return text

    # Tokenize words and remove stopwords
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word not in stop_words and word not in string.punctuation]

    # Compute word frequencies
    freq_dist = FreqDist(filtered_words)

    # Score sentences based on word importance
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in freq_dist:
                if sentence in sentence_scores:
                    sentence_scores[sentence] += freq_dist[word]
                else:
                    sentence_scores[sentence] = freq_dist[word]

    # Select top-ranked sentences
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
    return " ".join(summarized_sentences)

if __name__ == "__main__":
    # Path to the image for OCR
    image_path = "sample_image.png"  # Replace with your image path

    try:
        # Step 1: Extract text from image
        print("Performing OCR...")
        extracted_text = recognize_text_from_image(r"C:\Users\Devil\Desktop\bago")
        print("\nRecognized Text:")
        print(extracted_text)

        # Step 2: Summarize extracted text
        print("\nSummarizing Text...")
        summary = summarize_text_with_nltk(extracted_text)
        print("\nSummary:")
        print(summary)

    except Exception as e:
        print(f"Error: {e}")

        gray = cv2.cvtColor("image", cv2.COLOR_BGR2GRAY)
_, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
height, width = "image".shape[:2]
image = cv2.resize ("image") , (width * 2, height * 2)
