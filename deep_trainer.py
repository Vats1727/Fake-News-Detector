# deep_trainer.py
import pandas as pd
import numpy as np
import re
import string
import joblib
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# ==== PARAMETERS ====
MAX_VOCAB = 20000    # Max number of words to keep
MAX_LEN = 300        # Max length of news article
EMBEDDING_DIM = 128  # Size of word embedding vector

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # remove URLs
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\w*\d\w*', '', text)  # remove numbers
    return text

def train_lstm():
    # ==== LOAD DATA ====
    fake = pd.read_csv("./data/Fake.csv", encoding="latin1")
    real = pd.read_csv("./data/True.csv", encoding="latin1")

    # Merge into one dataframe
    fake["label"] = 0
    real["label"] = 1
    df = pd.concat([fake, real]).sample(frac=1).reset_index(drop=True)

    # Merge title and text if available
    if "title" in df.columns and "text" in df.columns:
        df["content"] = df["title"].astype(str) + " " + df["text"].astype(str)
    elif "Title" in df.columns and "Description" in df.columns:
        df["content"] = df["Title"].astype(str) + " " + df["Description"].astype(str)
    else:
        df["content"] = df[df.columns[0]].astype(str)

    # Clean text
    df["content"] = df["content"].apply(clean_text)

    X = df["content"].values
    y = df["label"].values

    # ==== TOKENIZE ====
    tokenizer = Tokenizer(num_words=MAX_VOCAB, oov_token="<OOV>")
    tokenizer.fit_on_texts(X)
    X_seq = tokenizer.texts_to_sequences(X)
    X_pad = pad_sequences(X_seq, maxlen=MAX_LEN, padding="post", truncating="post")

    # ==== SPLIT DATA ====
    X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.2, random_state=42)

    # ==== BUILD MODEL ====
    model = Sequential([
        Embedding(MAX_VOCAB, EMBEDDING_DIM, input_length=MAX_LEN),
        Bidirectional(LSTM(64, return_sequences=True)),
        Dropout(0.3),
        Bidirectional(LSTM(32)),
        Dense(32, activation="relu"),
        Dropout(0.3),
        Dense(1, activation="sigmoid")
    ])

    model.compile(loss="binary_crossentropy", optimizer=Adam(1e-3), metrics=["accuracy"])

    # ==== TRAIN ====
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=4,
        batch_size=64,
        verbose=1
    )

    # ==== SAVE ====
    os.makedirs("./model", exist_ok=True)
    model.save("./model/deep_model.h5")
    joblib.dump(tokenizer, "./model/tokenizer.pkl")

  
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f" Deep Learning Model Accuracy: {acc:.4f}")

if __name__ == "__main__":
    train_lstm()
