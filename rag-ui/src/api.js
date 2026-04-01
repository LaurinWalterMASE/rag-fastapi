import axios from "axios";

const API = axios.create({
  baseURL: "https://rag-fastapi-gpj3.onrender.com",
});

export const ingestPDF = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/ingest", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const queryLLM = (query) =>
  API.post("/query", { query });