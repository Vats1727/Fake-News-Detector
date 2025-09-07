import React, { useState } from "react";
import NewsForm from "./components/NewsForm";
import Result from "./components/Result";
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles/App.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="container text-center mt-5">
      <h1 className="mb-4">  News Headlines Detector</h1>
      <NewsForm setResult={setResult} />
      {result && <Result result={result} />}
    </div>
  );
}

export default App;
