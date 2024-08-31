const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  console.error("API URL is not defined. Please check your environment variables.");
  throw new Error("API URL is not defined. Please check your environment variables.");
}

console.log("API URL is: ", API_URL);

const defaultHeaders = {
  'Content-Type': 'application/json',
};

const request = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, options);
    if (!response.ok) {
      const errorMessage = `HTTP error! Status: ${response.status} - ${response.statusText}`;
      console.error(errorMessage);
      throw new Error(errorMessage);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error in API request:", error);
    throw error;
  }
};

export const uploadFiles = async (formData) => {
  const options = {
    method: 'POST',
    body: formData,
  };

  return await request('/upload', options);
};

export const fetchSummary = async () => {
  const data = await request('/summary');
  return data.summary || [];
};

export const fetchGroupedData = async (page = 1) => {
  return await request(`/grouped_data?page=${page}`);
};
