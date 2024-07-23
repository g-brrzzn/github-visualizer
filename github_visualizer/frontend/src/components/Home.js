import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setUsername(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim() !== '') {
      navigate(`/user/${username}`);
    }
  };

  return (
    <div className="home">
      <h1>Welcome to GitHub Visualizer</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter GitHub username"
          value={username}
          onChange={handleInputChange}
        />
        <button type="submit">Fetch Profile</button>
      </form>
    </div>
  );
};

export default Home;
