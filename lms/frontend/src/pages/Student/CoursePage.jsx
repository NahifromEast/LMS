import React, { useEffect, useState } from 'react';
import { getCourses } from '../../services/api'; // Make sure this function fetches your courses
import './CoursePage.css';

const CoursePage = () => {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getCourses();
      setCourses(data);
    };
    fetchData();
  }, []);

  return (
    <div className="course-page">
      <h2>Welcome to your course page!</h2>
      <div className="course-list">
        {courses.length ? (
          courses.map((course) => (
            <div key={course._id} className="course-card">
              <h4>{course.name}</h4>
              <p>Section: {course.section || 'N/A'}</p>
            </div>
          ))
        ) : (
          <p>No courses available.</p>
        )}
      </div>
    </div>
  );
};

export default CoursePage;