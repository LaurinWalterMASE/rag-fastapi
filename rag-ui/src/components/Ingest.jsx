import { useState } from "react";
import { ingestPDF } from "../api";

export default function Ingest() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleIngest = async () => {
    try {
      const res = await ingestPDF(file);
      setResult(JSON.stringify(res.data, null, 2));
    } catch (err) {
      setResult("Error: " + err.message);
    }
  };

  return (
    <div>
      <h2>Ingest PDF</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleIngest}>Ingest</button>

      <pre>{result}</pre>
    </div>
  );
}