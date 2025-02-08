import React, { useEffect, useState } from 'react';
import './InstructorDashboard.css'; // Import the CSS file

const InstructorDashboard = () => {
  const [instructorName, setInstructorName] = useState('Instructor'); // Default name
  const [stats, setStats] = useState({
    courses: 0,
    students: 0,
    pendingAssignments: 0,
  });
  const [recentActivity, setRecentActivity] = useState([]);

  // Simulate fetching data (Replace with actual API calls later)
  useEffect(() => {
    // Fetch instructor name
    setInstructorName('John Doe'); // Replace with API call to get name

    // Fetch stats
    setStats({
      courses: 3,
      students: 120,
      pendingAssignments: 5,
    });

    // Fetch recent activity
    setRecentActivity([
      'John Smith submitted Assignment 1',
      'Jane Doe left a comment on "Math 101"',
      'New student enrolled in "Science Basics"',
    ]);
  }, []);

  return (
    <div className="instructor-dashboard">
      <h1>Welcome, {instructorName}!</h1>
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>{stats.courses}</h3>
          <p>Courses</p>
        </div>
        <div className="stat-card">
          <h3>{stats.students}</h3>
          <p>Students</p>
        </div>
        <div className="stat-card">
          <h3>{stats.pendingAssignments}</h3>
          <p>Pending Assignments</p>
        </div>
      </div>
      <div className="recent-activity">
        <h2>Recent Activity</h2>
        <ul>
          {recentActivity.map((activity, index) => (
            <li key={index}>{activity}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default InstructorDashboard;