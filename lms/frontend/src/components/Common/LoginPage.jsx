import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../../services/api'; // Import API function to handle login
import './LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState(''); // Changed to 'email'
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate(); // To navigate after login

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await loginUser({ email, password }); // Changed 'username' to 'email'
      localStorage.setItem('token', response.token); // Save token to local storage
      localStorage.setItem('role', response.role); // Save role (admin/student)
      if (response.role === 'admin') {
        navigate('/dashboard'); // Redirect admin to dashboard
      } else {
        navigate('/courses'); // Redirect student to courses
      }
    } catch (error) {
      setError('Invalid email or password. Please try again.');
    }
  };

  return (
    <div className="login-page">
      <h1>Login</h1>
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label>Email:</label> {/* Updated label */}
          <input
            type="email"
            value={email} // Updated to 'email'
            onChange={(e) => setEmail(e.target.value)} // Updated to 'setEmail'
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p className="error">{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
