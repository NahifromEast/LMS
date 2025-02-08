import React from 'react';
import './Sidebar.css'; // Add CSS for styling the sidebar

const Sidebar = () => {
  return (
    <div className="sidebar">
      <ul>
        <li>Dashboard</li>
        <li>Courses</li>
        <li>Messages</li>
        <li>Settings</li>
      </ul>
    </div>
  );
};

export default Sidebar;