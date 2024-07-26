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

  const buildProfileInfo = (profile) => {
    let info = [];
    if (profile.location) info.push(profile.location);
    if (profile.company)  info.push(profile.company);
    if (profile.email)    info.push(profile.email);
    let result = info.join(' | ');
    if (result) result += ' |';
    return result;
  };

  if (!profile) {
    return <div className="center">Loading...</div>;
  }

  return (
    <div className="user-profile">
      <img src={profile.avatar_url} alt={`${profile.name}'s avatar`} className="profile-avatar" />
      <hr />
      <h1>{profile.name}</h1>
      <p id="tab">{profile.bio}</p>
      <p id="tab">{buildProfileInfo(profile)} Followers: {profile.followers} | Following: {profile.following}</p>

      <h2>Repositories</h2>
      <div className="repo-grid">
        {repositories.map(repo => (
          <div key={repo.id} className="repo-item">
            <h3>{repo.name}</h3>
            <p>{repo.description}</p>
            <p>Stars: {repo.stargazers_count}</p>
            <p>Forks: {repo.forks_count}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UserProfile;
