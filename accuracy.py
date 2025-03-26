import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

try:
    # Load data (ensure file exists and has correct structure)
    data = pd.read_csv('your_dataset.csv')

    # Check for missing values and handle them
    if data.isnull().any().any():
        data = data.dropna()  # Option to drop rows with missing values
        print("Warning: Missing values were removed.")
    
    # Preprocess data
    X = data.drop('target', axis=1)  # Features
    y = data['target']  # Target variable

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f'Accuracy: {accuracy:.2f}')

except FileNotFoundError:
    print(r"C:\\Users\\Devil\Desktop\\bago")
except KeyError as e:
    print(f"Error: Missing required column - {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

