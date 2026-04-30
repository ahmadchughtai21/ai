import React from 'react';
import { useTheme } from '../context/ThemeContext';

const Navbar = ({ user, onLogout, onAddTask, onToggleSidebar, onToggleChat }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="navbar">
      <div className="navbar-brand-group">
        <button className="mobile-menu-toggle" onClick={onToggleSidebar} title="Toggle Menu">
          ☰
        </button>
        <h1>TackTack</h1>
      </div>
      <div className="navbar-actions">
        <span className="navbar-user-chip">{user?.username}</span>
        <button className="mobile-menu-toggle" onClick={onToggleChat} title="Toggle AI Chat">
          💬
        </button>
        <button className="add-task-btn" onClick={onAddTask}>
          <span>+</span>
          <span className="new-task-label">New Task</span>
        </button>
        <button className="theme-toggle" onClick={toggleTheme} title="Toggle Theme">
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
        <button className="logout-btn" onClick={onLogout} title="Logout">
          <span className="logout-label">Logout</span>
          <span className="logout-icon" aria-hidden="true">↩</span>
        </button>
      </div>
    </div>
  );
};

export default Navbar;
