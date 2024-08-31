// app/api/api.js

const API_URL = 'http://localhost:8000/api/v1';

export const uploadFiles = async (formData) => {
  const response = await axios.post(`${API_URL}/upload`, formData);
  return response.data;
};

export const fetchSummary = async () => {
  const response = await fetch(`${API_URL}/summary`);
  return response.data;
};

export const fetchGroupedData = async () => {
  const response = await fetch(`${API_URL}/grouped_data`);
  return response.data;
};
