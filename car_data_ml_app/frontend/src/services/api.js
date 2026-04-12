import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`${API_BASE}/upload/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const getSummary = async () => {
  const response = await axios.get(`${API_BASE}/analyze/summary`);
  return response.data;
};

export const getEdaSummary = async () => {
  const response = await axios.get(`${API_BASE}/eda/summary`);
  return response.data;
};

export const getScatterData = async (x, y) => {
  const response = await axios.get(`${API_BASE}/eda/scatter`, { params: { x, y } });
  return response.data;
};

export const preprocessData = async (options) => {
  const response = await axios.post(`${API_BASE}/preprocess/`, options);
  return response.data;
};

export const trainRegression = async (params) => {
  const response = await axios.post(`${API_BASE}/regression/train`, params);
  return response.data;
};

export const trainClassification = async (params) => {
  const response = await axios.post(`${API_BASE}/classification/train`, params);
  return response.data;
};

export const getPca = async () => {
  const response = await axios.get(`${API_BASE}/pca/`);
  return response.data;
};

export const trainKmeans = async (params) => {
  const response = await axios.post(`${API_BASE}/clustering/kmeans`, params);
  return response.data;
};

export const getFeatureRank = async (target = 'price') => {
  const response = await axios.get(`${API_BASE}/features/rank`, { params: { target } });
  return response.data;
};

export const getHierarchical = async () => {
  const response = await axios.get(`${API_BASE}/clustering/hierarchical`);
  return response.data;
};
