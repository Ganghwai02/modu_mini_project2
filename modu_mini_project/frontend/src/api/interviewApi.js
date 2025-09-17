// frontend/src/api/interviewApi.js

import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: BASE_URL,
});

export const getInterviewQuestion = async (chatHistory, jobTitle = null) => {
  try {
    const response = await api.post('/interview/question', { chatHistory, jobTitle });
    return response.data;
  } catch (error) {
    console.error('Error fetching interview question:', error);
    throw error;
  }
};

export const getFeedback = async (chatHistory) => {
  try {
    const response = await api.post('/interview/feedback', { chatHistory });
    return response.data;
  } catch (error) {
    console.error('Error fetching feedback:', error);
    throw error;
  }
};