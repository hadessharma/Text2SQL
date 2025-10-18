import axios from 'axios';
import dotenv from 'dotenv';
// Base API configuration
dotenv.config();

const API_BASE_URL = process.env.API_BASE_URL;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints as specified in the README
export const apiService = {
  // Submit schema and generate Knowledge Graph
  submitSchema: async (schemaData) => {
    try {
      const response = await api.post('/submit-schema', schemaData);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to submit schema: ${error.message}`);
    }
  },

  // Generate SQL from natural language query
  generateSQL: async (queryData) => {
    try {
      const response = await api.post('/generate-sql', queryData);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to generate SQL: ${error.message}`);
    }
  },
};

export default api;
