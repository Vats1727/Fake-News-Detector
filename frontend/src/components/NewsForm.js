import React, { useState } from "react";
import axios from "axios";

function NewsForm({ setResult }) {
  const [url, setUrl] = useState("");
  const [title, setTitle] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);

    try {
      const response = await axios.post("https://fake-news-detector-backend-yk7u.onrender.com/predict", {
        url,
        title,
      });
      setResult(response.data);
    } catch (error) {
      setResult({ error: "Error fetching prediction" });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card p-4 shadow">
      <div className="mb-3">
        <label className="form-label">Paste News Article URL:</label>
        <input
          type="url"
          className="form-control"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com/article"
        />
      </div>

      <div className="text-center">— OR —</div>

      <div className="mb-3">
        <label className="form-label">Enter Headline/Title:</label>
        <input
          type="text"
          className="form-control"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter headline"
        />
      </div>

      <button type="submit" className="btn btn-primary w-100">
        Check News
      </button>
    </form>
  );
}

export default NewsForm;
