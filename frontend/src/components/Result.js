import React from "react";

function Result({ result }) {
  if (result.error) {
    return <div className="alert alert-danger mt-3">{result.error}</div>;
  }

  return (
    <div className="card mt-4 p-3 shadow">
      <h4>Prediction Result</h4>
      <p><b>Headline:</b> {result.headline}</p>
      <p><b>Result:</b> {result.result}</p>
      <p><b>Confidence:</b> {result.confidence}</p>
    </div>
  );
}

export default Result;
