import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier  # <--- NEW HERO
from sklearn.metrics import accuracy_score
import joblib
import os

# Configuration
DATA_PATH = "./data/train.csv"
MODEL_DIR = "./backend/app/resources"
MODEL_PATH = os.path.join(MODEL_DIR, "toxic_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)


def train():
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)

    # Handle missing values
    df['comment_text'] = df['comment_text'].fillna('')

    # Define features and ALL target labels
    X = df['comment_text']
    # The 6 specific labels from the Kaggle dataset
    target_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    y = df[target_cols]

    print(f"Targets: {target_cols}")

    # Split Data
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build Pipeline
    print("Training Multi-Label model...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=10000)),  # Increased features for better accuracy
        # MultiOutputClassifier trains one regressor per column automatically
        ('clf', MultiOutputClassifier(LogisticRegression(solver='liblinear')))
    ])

    pipeline.fit(X_train, y_train)

    # Evaluate
    print("Evaluating...")
    predictions = pipeline.predict(X_test)
    # Average accuracy across all labels
    print(f"Overall Accuracy: {pipeline.score(X_test, y_test):.4f}")

    # Save the Pipeline AND the list of column names
    # We save a dictionary so the backend knows what the 0,1,2... indexes mean
    print(f"Saving model to {MODEL_PATH}...")
    model_data = {
        "pipeline": pipeline,
        "labels": target_cols
    }
    joblib.dump(model_data, MODEL_PATH)
    print("Done!")


if __name__ == "__main__":
    train()
