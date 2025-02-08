import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api'; // Your Django API

export const getCourses = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/get_courses/`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch courses', error);
    return [];
  }
};


export const loginUser = async (credentials) => {
  const response = await fetch('http://127.0.0.1:8000/api/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    throw new Error('Failed to login');
  }

  return await response.json();
};