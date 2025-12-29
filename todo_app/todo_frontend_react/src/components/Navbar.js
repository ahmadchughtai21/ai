import React from 'react';
import { useTheme } from '../context/ThemeContext';

const Navbar = ({ onAddTask }) => {
  const { toggleTheme } = useTheme();

  return (
    <div className="navbar">
      <h1>✓ AI Manager</h1>
      <div className="navbar-actions">
        <button className="add-task-btn" onClick={onAddTask}>
          <span>+</span>
          <span>New Task</span>
        </button>
        <button className="theme-toggle" onClick={toggleTheme}>
          🌓 Theme
        </button>
      </div>
    </div>
  );
};

export default Navbar;
