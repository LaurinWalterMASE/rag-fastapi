import { useState } from "react";
import { ingestPDF } from "../api";

export default function Ingest() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setResult("Please select a file");
      return;
    }

    try {
      const res = await ingestPDF(file);
      setResult(JSON.stringify(res.data, null, 2));
    } catch (err) {
      setResult("Error: " + err.message);
    }
  };

  return (
    <div>
      <h2> Upload PDF</h2>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>Upload & Ingest</button>

      <pre>{result}</pre>
    </div>
  );
}