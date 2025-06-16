import React from "react";
import { Link } from "react-router-dom";


const Home = () => {
 
  return (
    <div className="dashboard">
      <h2>Welcome, {currentUser.name || currentUser.username}</h2>
      
      <div className="user-card">
        <p><strong>Name:</strong> {currentUser.name || "N/A"}</p>
        <p><strong>Email:</strong> {currentUser.email || "N/A"}</p>
        
      </div>

  
    </div>
  );
};

export default Home;
