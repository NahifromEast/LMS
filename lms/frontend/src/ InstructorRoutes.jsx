import React from 'react';
import { Routes, Route } from 'react-router-dom';
import InstructorDashboard from './pages/Instructor/InstructorDashboard/InstructorDashboard';
import InstructorCourses from './pages/Instructor/InstructorCourses/InstructorCourses';
import InstructorContent from './pages/Instructor/InstructorContent/InstructorContent';

const InstructorRoutes = () => {
  return (
    <Routes>
      <Route path="/instructor/dashboard" element={<InstructorDashboard />} />
      <Route path="/instructor/courses" element={<InstructorCourses />} />
      <Route path="/instructor/content" element={<InstructorContent />} />
    </Routes>
  );
};

export default InstructorRoutes;