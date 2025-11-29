import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib
import os

# 1. Configuration
# Make sure this path points to where you unzipped the Kaggle data
DATA_PATH = "./data/train.csv"
MODEL_DIR = "./backend/app/resources"
MODEL_PATH = os.path.join(MODEL_DIR, "toxic_model.pkl")

# Create the backend resources directory if it doesn't exist yet
os.makedirs(MODEL_DIR, exist_ok=True)


def train():
    print("Loading data...")
    # Load only the necessary columns to save memory
    df = pd.read_csv(DATA_PATH)

    # We will focus on the 'toxic' label for this MVP
    # Handle missing values in text (just in case)
    df['comment_text'] = df['comment_text'].fillna('')

    X = df['comment_text']
    y = df['toxic']

    # 2. Split Data (80% training, 20% testing)
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Build Pipeline
    # TfidfVectorizer: Converts text to numbers based on word frequency
    # LogisticRegression: The classification algorithm
    print("Training model (this might take a minute)...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),  # Limit to top 5k words to keep model small
        ('clf', LogisticRegression())
    ])

    pipeline.fit(X_train, y_train)

    # 4. Evaluate
    print("Evaluating model...")
    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy:.4f}")

    # 5. Save the Pipeline
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(pipeline, MODEL_PATH)
    print("Done!")


if __name__ == "__main__":
    train()