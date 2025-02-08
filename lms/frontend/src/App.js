import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import InstructorRoutes from './InstructorRoutes'; 
import StudentRoutes from './StudentRoutes';       
import ManagerRoutes from './ManagerRoutes';       
import AdminRoutes from './AdminRoutes';           
import LoginPage from './components/Common/LoginPage';    

function App() {
  const userRole = localStorage.getItem('role'); // Example: 'admin', 'manager', 'instructor', 'student'

  return (
    <BrowserRouter>
      {/* Route based on user role */}
      {userRole === 'instructor' && <InstructorRoutes />}
      {userRole === 'student' && <StudentRoutes />}
      {userRole === 'manager' && <ManagerRoutes />}
      {userRole === 'admin' && <AdminRoutes />}
      {!userRole && <LoginPage />} {/* Default to login if no role is found */}
    </BrowserRouter>
  );
}

export default App;
