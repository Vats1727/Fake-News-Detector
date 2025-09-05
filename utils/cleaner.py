
import pandas as pd
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def clean_and_train():

    try:
        fake = pd.read_csv('./data/Fake.csv', encoding="utf-8-sig", low_memory=False)
    except UnicodeDecodeError:
        fake = pd.read_csv('./data/Fake.csv', encoding="ISO-8859-1", low_memory=False)

    try:
        real = pd.read_csv('./data/True.csv', encoding="utf-8-sig", low_memory=False)
    except UnicodeDecodeError:
        real = pd.read_csv('./data/True.csv', encoding="ISO-8859-1", low_memory=False)

    # Ensure proper column names
    if "Title" in fake.columns and "Description" in fake.columns:
        fake["text"] = fake["Title"].astype(str) + " " + fake["Description"].astype(str)
    elif "title" in fake.columns and "text" in fake.columns:
        fake["text"] = fake["title"].astype(str) + " " + fake["text"].astype(str)
    else:
        fake["text"] = fake.iloc[:, 0].astype(str)  

    if "Title" in real.columns and "Description" in real.columns:
        real["text"] = real["Title"].astype(str) + " " + real["Description"].astype(str)
    elif "title" in real.columns and "text" in real.columns:
        real["text"] = real["title"].astype(str) + " " + real["text"].astype(str)
    else:
        real["text"] = real.iloc[:, 0].astype(str)  

    # Add labels
    fake['label'] = 0  # FAKE
    real['label'] = 1  # REAL

  
    df = pd.concat([fake, real]).sample(frac=1).reset_index(drop=True)

    # Clean text
    df['text'] = df['text'].str.lower().str.translate(str.maketrans('', '', string.punctuation))

    X = df['text']
    y = df['label']

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
    X_vect = vectorizer.fit_transform(X)

    # Model training
    model = PassiveAggressiveClassifier(max_iter=1000)
    model.fit(X_vect, y)

    # Saving model and vectorizer
    os.makedirs('./model', exist_ok=True)
    joblib.dump(model, './model/classifier.pkl')
    joblib.dump(vectorizer, './model/vectorizer.pkl')

    # Evaluate
    X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)
    predictions = model.predict(X_test)
    print(" Accuracy:", accuracy_score(y_test, predictions))

if __name__ == "__main__":
    clean_and_train()
