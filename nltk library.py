import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Download NLTK resources
nltk.download('punkt')

# Example dataset
corpus = [
    "I love programming.",
    "Python is amazing!",
    "Coding is fun.",
    "I enjoy learning.",
    "Programming is great."
]
labels = [1, 1, 1, 0, 1]  # Binary labels (e.g., 1 = Positive, 0 = Neutral)

# Tokenize and preprocess text using NLTK
def preprocess_text(corpus):
    processed_corpus = [] 
    for text in corpus:
        tokens = nltk.word_tokenize(text.lower())
        processed_corpus.append(' '.join(tokens))
    return processed_corpus

processed_corpus = preprocess_text(corpus)

# Extract features using CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(processed_corpus)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Predict and evaluate
y_pred = classifier.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")


from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

# Sample training data
training_data = [
    ({'text': 'love the food'}, 'positive'),
    ({'text': 'hate the service'}, 'negative')
]

# Train model
classifier = NaiveBayesClassifier.train(training_data)

# Test accuracy
print(f"Accuracy: {accuracy(classifier, training_data)}")


from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
words = [lemmatizer.lemmatize(word) for word in tokens]=[]

