#!/usr/bin/env python3
"""
Script to retrain the machine learning models with the current scikit-learn version
to fix compatibility issues.
"""

import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import nltk
import os

def download_nltk_requirements():
    """Download required NLTK data if not already present."""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords')
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt')

def preprocess_text(comments):
    """Preprocess comments similar to the original processing."""
    stops = set(stopwords.words('english'))
    stops.add("'")
    stops.add("<br>")
    stops.add("<br />")
    
    processed_comments = []
    
    for comment in comments:
        # Convert to string and lowercase
        comment = str(comment).lower()
        
        # Remove stopwords
        words = comment.split()
        filtered_words = [word for word in words if word not in stops]
        comment_without_sw = " ".join(filtered_words)
        
        # Clean with regex - keep only letters and spaces
        cleaned_comment = re.sub(r'[^a-zA-Z ]', ' ', comment_without_sw)
        
        # Remove extra spaces
        cleaned_comment = re.sub(r'\s+', ' ', cleaned_comment).strip()
        
        processed_comments.append(cleaned_comment)
    
    return processed_comments

def retrain_models():
    """Retrain the models with current scikit-learn version."""
    print("Starting model retraining...")
    
    # Download NLTK requirements
    download_nltk_requirements()
    
    # Load the training data
    data_path = os.path.join("final_Data", "final.csv")
    if not os.path.exists(data_path):
        print(f"Training data not found at {data_path}")
        return False
    
    print("Loading training data...")
    df = pd.read_csv(data_path)
    
    # Extract features and labels
    comments = df['comment_text'].values
    sentiments = df['pol'].values
    
    print(f"Loaded {len(comments)} training samples")
    
    # Preprocess the comments
    print("Preprocessing comments...")
    processed_comments = preprocess_text(comments)
    
    # Create TF-IDF vectorizer
    print("Creating TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,  # Limit features to prevent memory issues
        lowercase=True,
        stop_words='english',
        ngram_range=(1, 2)  # Use unigrams and bigrams
    )
    
    # Fit and transform the comments
    X = vectorizer.fit_transform(processed_comments)
    y = sentiments
    
    print(f"Vectorized comments shape: {X.shape}")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate the model
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the models
    print("Saving models...")
    joblib.dump(vectorizer, "vectorized.pkl")
    joblib.dump(model, "random_forest.pkl")
    
    # Also save backup files
    joblib.dump(vectorizer, "vectorized_backup.pkl")
    joblib.dump(model, "random_forest_backup.pkl")
    
    print("Models saved successfully!")
    print("- vectorized.pkl (TF-IDF vectorizer)")
    print("- random_forest.pkl (Random Forest model)")
    print("- Backup files also created")
    
    return True

if __name__ == "__main__":
    success = retrain_models()
    if success:
        print("\nModel retraining completed successfully!")
    else:
        print("\nModel retraining failed!")