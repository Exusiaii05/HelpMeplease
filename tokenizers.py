import re
import string
import zipfile
import nltk

# Utilities
def normalize_language(language):
    """Normalize language codes (e.g., en-US -> en)."""
    return language.lower().split('-')[0]

def to_string(value):
    """Convert bytes to string."""
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return str(value)

def to_unicode(value):
    """Ensure the value is unicode (string in Python 3)."""
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value

unicode = str  # Python 3 compatibility

class DefaultWordTokenizer(object):
    """Default NLTK word tokenizer."""
    def tokenize(self, text):
        return nltk.word_tokenize(text)

# Specialized Tokenizers
class HebrewWordTokenizer:
    """Tokenize Hebrew text."""
    _TRANSLATOR = str.maketrans("", "", string.punctuation)

    @classmethod
    def tokenize(cls, text):
        try:
            from hebrew_tokenizer import tokenize
            from hebrew_tokenizer.groups import Groups
        except ImportError:
            raise ValueError("Hebrew tokenizer requires 'hebrew_tokenizer'. Install it with 'pip install hebrew_tokenizer'.")
        
        text = text.translate(cls._TRANSLATOR)
        return [
            word for token, word, _, _ in tokenize(text)
            if token in (Groups.HEBREW, Groups.HEBREW_1, Groups.HEBREW_2)
        ]

# Add other tokenizers (Japanese, Chinese, etc.) following the same pattern.

class Tokenizer(object):
    """Language-dependent tokenizer for text documents."""
    _WORD_PATTERN = re.compile(r"^[^\W\d_](?:[^\W\d_]|['-])*$", re.UNICODE)
    
    # Map language aliases (e.g., Slovak -> Czech)
    LANGUAGE_ALIASES = {
        "slovak": "czech",
    }

    def __init__(self, language):
        language = normalize_language(language)
        self._language = language
        tokenizer_language = self.LANGUAGE_ALIASES.get(language, language)
        self._sentence_tokenizer = self._get_sentence_tokenizer(tokenizer_language)
        self._word_tokenizer = self._get_word_tokenizer(tokenizer_language)

    @property
    def language(self):
        return self._language

    def _get_sentence_tokenizer(self, language):
        """Load or download the sentence tokenizer for the specified language."""
        try:
            return nltk.data.load(f"tokenizers/punkt/{language}.pickle")
        except (LookupError, zipfile.BadZipfile):
            nltk.download('punkt')  # Ensure Punkt tokenizer is available
            return nltk.data.load(f"tokenizers/punkt/{language}.pickle")

    def _get_word_tokenizer(self, language):
        """Return the appropriate word tokenizer based on language."""
        # You can extend the logic here to return different tokenizers based on the language
        return DefaultWordTokenizer()

    def to_sentences(self, paragraph):
        """Tokenize the given paragraph into sentences."""
        return tuple(map(str.strip, self._sentence_tokenizer.tokenize(to_unicode(paragraph))))

    def to_words(self, sentence):
        """Tokenize the given sentence into words."""
        words = self._word_tokenizer.tokenize(to_unicode(sentence))
        return tuple(filter(self._is_word, words))

    @staticmethod
    def _is_word(word):
        """Check if the token matches the word pattern."""
        return bool(Tokenizer._WORD_PATTERN.match(word))

# Usage example
if __name__ == "__main__":
    text = "This is a sample paragraph. It has multiple sentences."
    tokenizer = Tokenizer("english")
    
    print("Sentences:", tokenizer.to_sentences(text))
    print("Words:", tokenizer.to_words(text))

