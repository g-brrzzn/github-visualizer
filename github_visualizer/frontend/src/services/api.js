import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const fetchUserProfile = async (username) => {
  try {
    const response = await axios.get(`${API_URL}/profile/${username}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching user profile", error);
    throw error;
  }
};
