export const ingestPDF = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/ingest", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};