import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchUserProfile } from '../services/api';
import './UserProfile.css';

const UserProfile = () => {
  const { username } = useParams();
  const [profile, setProfile] = useState(null);
  const [repositories, setRepositories] = useState([]);

  useEffect(() => {
    const getUserProfile = async () => {
      try {
        const data = await fetchUserProfile(username);
        setProfile(data.profile);
        setRepositories(data.repositories);
      } catch (error) {
        console.error("Error fetching user profile", error);
      }
    };

    getUserProfile();
  }, [username]);

  if (!profile) {
    return <div>Loading...</div>;
  }

  return (
    <div className="user-profile">
      <h1>{profile.name}</h1>
      <p>{profile.bio}</p>
      <h2>Repositories</h2>
      <ul>
        {repositories.map(repo => (
          <li key={repo.id}>
            <h3>{repo.name}</h3>
            <p>{repo.description}</p>
            <p>Stars: {repo.stargazers_count}</p>
            <p>Forks: {repo.forks_count}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserProfile;
