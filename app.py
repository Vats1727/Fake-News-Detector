# app.py
from flask import Flask, request, jsonify
import joblib
import newspaper
from flask_cors import CORS
import os

app = Flask(__name__)

# Allow only your frontend domain (Vercel) to access
CORS(app, resources={r"/*": {"origins": "https://news-headline-detector.vercel.app"}})

# Load trained model + vectorizer
model = joblib.load("./model/classifier.pkl")
vectorizer = joblib.load("./model/vectorizer.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    url = data.get("url")
    title = data.get("title")
    news_text = ""

    # Extract title from URL if provided
    if url:
        try:
            article = newspaper.Article(url)
            article.download()
            article.parse()
            news_text = article.title.strip()
        except Exception as e:
            return jsonify({"error": f"Error extracting title: {str(e)}"}), 400

    elif title:
        news_text = title.strip()
    else:
        return jsonify({"error": "No input provided"}), 400

    # Vectorize & predict
    vect_text = vectorizer.transform([news_text])
    prediction = model.predict(vect_text)[0]
    proba = model.decision_function(vect_text)[0]

    result = "It Seems Real News" if prediction == 1 else "It Seems Fake News"
    confidence = round(abs(proba) * 100, 2)

    return jsonify({
        "headline": news_text,
        "result": result,
        "confidence": f"{confidence}%"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
