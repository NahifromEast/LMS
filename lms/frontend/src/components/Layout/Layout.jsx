import React from 'react';
import Sidebar from '../Common/Sidebar';
import Navbar from '../Common/Navbar';
import './Layout.css';

const Layout = ({ children }) => {
  return (
    <div className="layout">
      <Sidebar />
      <div className="main-content">
        <Navbar />
        <div className="content">{children}</div>
      </div>
    </div>
  );
};

export default Layout;