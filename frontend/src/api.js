import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8001/api',
});

export const metadataAPI = {
  getAll: () => api.get('/schema/metadata'),
  getQuality: (tableName) => api.get(`/schema/quality/${tableName}`),
  getDocumentation: (tableName) => api.get(`/schema/documentation/${tableName}`),
  exportJSON: () => api.get('/schema/export/json'),
};

export const chatAPI = {
  sendMessage: (question) => api.post('/chat/chat', { question }),
};

export default api;
