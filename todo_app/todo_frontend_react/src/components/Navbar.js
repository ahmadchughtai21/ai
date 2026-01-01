import React from 'react';
import { useTheme } from '../context/ThemeContext';

const Navbar = ({ onAddTask, onToggleSidebar, onToggleChat }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="navbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button className="mobile-menu-toggle" onClick={onToggleSidebar} title="Toggle Menu">
          ☰
        </button>
        <h1>TackTack</h1>
      </div>
      <div className="navbar-actions">
        <button className="mobile-menu-toggle" onClick={onToggleChat} title="Toggle AI Chat">
          💬
        </button>
        <button className="add-task-btn" onClick={onAddTask}>
          <span>+</span>
          <span>New Task</span>
        </button>
        <button className="theme-toggle" onClick={toggleTheme} title="Toggle Theme">
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
      </div>
    </div>
  );
};

export default Navbar;
