import { useState } from "react";
import { queryLLM } from "../api";
export default function Query() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const handleQuery = async () => {
    try {
      const res = await queryLLM(question);
      setAnswer(res.data.answer);
    } catch (err) {
      setAnswer("Error: " + err.message);
    }
  };
  return (
    <div>
      <h2>Ask Question</h2>
      <input
        type="text"
        placeholder="Ask something..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={handleQuery}>Ask</button>
      <p><strong>Answer:</strong> {answer}</p>
    </div>
  );
}