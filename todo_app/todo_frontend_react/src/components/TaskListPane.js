import React, { useState } from 'react';
import { updateTask } from '../services/api';

const TaskListPane = ({ tasks, onTaskSelect, selectedTaskId, onTaskToggle, onSearch }) => {
  const [completedCollapsed, setCompletedCollapsed] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    onSearch(value);
  };

  const pendingTasks = tasks.filter(t => t.status === 'pending');
  const completedTasks = tasks.filter(t => t.status === 'completed');

  const today = new Date().toISOString().split('T')[0];
  const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];

  const overdue = pendingTasks.filter(t => t.due_date_only && t.due_date_only < today);
  const todayTasks = pendingTasks.filter(t => t.due_date_only === today);
  const tomorrowTasks = pendingTasks.filter(t => t.due_date_only === tomorrow);
  const laterTasks = pendingTasks.filter(t =>
    !t.due_date_only || (t.due_date_only > tomorrow)
  );

  const handleTaskToggle = async (taskId, currentStatus) => {
    const newStatus = currentStatus === 'pending' ? 'completed' : 'pending';
    try {
      await updateTask(taskId, { status: newStatus });
      onTaskToggle();
    } catch (error) {
      console.error('Error toggling task:', error);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    const today = new Date().toISOString().split('T')[0];
    const tomorrow = new Date(Date.now() + 86400000).toISOString().split('T')[0];

    if (dateStr === today) return 'Today';
    if (dateStr === tomorrow) return 'Tomorrow';

    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const renderTaskItem = (task) => {
    const isCompleted = task.status === 'completed';
    const isSelected = selectedTaskId === task.id;

    let priorityBadge = '';
    if (task.priority && task.priority !== 'none') {
      priorityBadge = (
        <span className={`task-badge priority-${task.priority}`}>
          {task.priority.toUpperCase()}
        </span>
      );
    }

    const tags = (task.tags || []).map(tag => (
      <span key={tag.id} className="task-tag">#{tag.name}</span>
    ));

    const category = task.category_name && task.category_name !== 'Inbox' && (
      <span className="task-category">
        <span className="category-color" style={{ backgroundColor: task.category_detail?.color }}></span>
        {task.category_name}
      </span>
    );

    const dueDate = task.due_date_only && (
      <span className={`task-due ${task.due_date_only < today ? 'overdue' : ''}`}>
        📅 {formatDate(task.due_date_only)} {task.due_time || ''}
      </span>
    );

    return (
      <div
        key={task.id}
        className={`task-item ${isSelected ? 'selected' : ''}`}
        onClick={() => onTaskSelect(task.id)}
      >
        <div className="task-header">
          <input
            type="checkbox"
            className="task-checkbox"
            checked={isCompleted}
            onChange={(e) => {
              e.stopPropagation();
              handleTaskToggle(task.id, task.status);
            }}
          />
          <div className="task-content">
            <div className={`task-title ${isCompleted ? 'completed' : ''}`}>
              {task.title}
            </div>
            {(priorityBadge || tags.length > 0 || category || dueDate) && (
              <div className="task-meta">
                {priorityBadge}
                {category}
                {tags}
                {dueDate}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  if (tasks.length === 0) {
    return (
      <div className="task-list-pane">
        <div className="task-pane-header">
          <input
            type="text"
            className="task-search-input"
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={handleSearch}
          />
        </div>
        <div className="task-list-content">
          <div className="empty-state">
            <div className="empty-state-icon">📭</div>
            <div>No tasks found</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="task-list-pane">
      <div className="task-pane-header">
        <input
          type="text"
          className="task-search-input"
          placeholder="Search tasks..."
          value={searchQuery}
          onChange={handleSearch}
        />
      </div>
      <div className="task-list-content">
      {overdue.length > 0 && (
        <div className="task-section">
          <div className="section-header">⚠️ Overdue</div>
          {overdue.map(renderTaskItem)}
        </div>
      )}

      {todayTasks.length > 0 && (
        <div className="task-section">
          <div className="section-header">📅 Today</div>
          {todayTasks.map(renderTaskItem)}
        </div>
      )}

      {tomorrowTasks.length > 0 && (
        <div className="task-section">
          <div className="section-header">🌅 Tomorrow</div>
          {tomorrowTasks.map(renderTaskItem)}
        </div>
      )}

      {laterTasks.length > 0 && (
        <div className="task-section">
          <div className="section-header">📆 Later</div>
          {laterTasks.map(renderTaskItem)}
        </div>
      )}

      {completedTasks.length > 0 && (
        <div className="task-section completed-section">
          <div
            className="section-header collapsible"
            onClick={() => setCompletedCollapsed(!completedCollapsed)}
          >
            <span className={`section-toggle ${completedCollapsed ? 'collapsed' : ''}`}>
              ▼
            </span>
            ✅ Completed ({completedTasks.length})
          </div>
          {!completedCollapsed && (
            <div className="completed-tasks">
              {completedTasks.map(renderTaskItem)}
            </div>
          )}
        </div>
      )}
      </div>
    </div>
  );
};

export default TaskListPane;
