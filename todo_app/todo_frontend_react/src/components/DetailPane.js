import React, { useState, useEffect, useCallback } from 'react';
import { getTask, deleteTask, toggleSubtaskComplete, deleteAttachment } from '../services/api';

const DetailPane = ({ taskId, onTaskDeleted, onTaskUpdated, onEditTask, refreshTrigger, className = '', onClose }) => {
  const [task, setTask] = useState(null);

  const loadTask = useCallback(async () => {
    if (!taskId) return;

    try {
      const response = await getTask(taskId);
      setTask(response.data);
    } catch (error) {
      console.error('Error loading task:', error);
    }
  }, [taskId]);

  useEffect(() => {
    if (taskId) {
      loadTask();
    } else {
      setTask(null);
    }
  }, [taskId, refreshTrigger, loadTask]);

  const handleDeleteTask = async () => {
    if (!window.confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
      return;
    }

    try {
      await deleteTask(taskId);
      onTaskDeleted();
    } catch (error) {
      console.error('Error deleting task:', error);
      alert('Failed to delete task');
    }
  };

  const handleEditTask = () => {
    if (onEditTask && task) {
      onEditTask(task);
    }
  };

  const handleToggleSubtask = async (subtaskId) => {
    try {
      await toggleSubtaskComplete(subtaskId);
      loadTask(); // Reload to get updated subtask status
      onTaskUpdated();
    } catch (error) {
      console.error('Error toggling subtask:', error);
    }
  };

  const handleDeleteAttachment = async (attachmentId) => {
    if (!window.confirm('Delete this attachment?')) {
      return;
    }

    try {
      await deleteAttachment(attachmentId);
      loadTask();
      onTaskUpdated();
    } catch (error) {
      console.error('Error deleting attachment:', error);
      alert('Failed to delete attachment');
    }
  };

  if (!task) {
    return (
      <div className={`detail-pane empty ${className}`}>
        <div className="empty-state">
          <div className="empty-state-icon">📝</div>
          <div>Select a task to view details</div>
        </div>
      </div>
    );
  }

  const priorityColor = {
    'high': 'var(--priority-high)',
    'medium': 'var(--priority-medium)',
    'low': 'var(--priority-low)'
  }[task.priority] || 'var(--text-muted)';

  return (
    <div className={`detail-pane ${className}`}>
      {onClose && (
        <button 
          className="mobile-close-btn" 
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '16px',
            right: '16px',
            background: 'var(--bg-secondary)',
            border: '1px solid var(--border-color)',
            borderRadius: '50%',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            fontSize: '18px',
            zIndex: 10
          }}
        >
          ×
        </button>
      )}
      <div className="detail-header">
        <div>
          <div className="detail-title">{task.title}</div>
        </div>
        <div className="detail-actions">
          <button className="icon-btn" onClick={handleEditTask} title="Edit task">
            ✏️
          </button>
          <button className="icon-btn danger" onClick={handleDeleteTask} title="Delete task">
            🗑️
          </button>
        </div>
      </div>

      {task.description && (
        <div className="detail-section">
          <div className="detail-section-title">Description</div>
          <div className="detail-description">{task.description}</div>
        </div>
      )}

      <div className="detail-section">
        <div className="detail-section-title">Details</div>

        <div className="info-row">
          <span className="info-label">Status:</span>
          <span className="info-value" style={{
            color: task.status === 'completed' ? 'var(--accent-green)' : 'var(--accent-blue)'
          }}>
            {task.status === 'completed' ? '✅ Completed' : '⏳ Pending'}
          </span>
        </div>

        <div className="info-row">
          <span className="info-label">Priority:</span>
          <span className="info-value" style={{ color: priorityColor }}>
            {task.priority ? task.priority.charAt(0).toUpperCase() + task.priority.slice(1) : 'None'}
          </span>
        </div>

        {task.category_name && (
          <div className="info-row">
            <span className="info-label">Category:</span>
            <span className="info-value">
              <span
                className="category-color"
                style={{
                  backgroundColor: task.category_detail?.color,
                  display: 'inline-block',
                  marginRight: '6px'
                }}
              ></span>
              {task.category_name}
            </span>
          </div>
        )}

        {task.due_date_only && (
          <div className="info-row">
            <span className="info-label">Due Date:</span>
            <span className="info-value">
              {new Date(task.due_date_only).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
              })}
              {task.due_time && ` at ${task.due_time}`}
            </span>
          </div>
        )}

        {task.recurrence && task.recurrence !== 'none' && (
          <div className="info-row">
            <span className="info-label">Repeats:</span>
            <span className="info-value" style={{ color: 'var(--accent-blue)' }}>
              🔁 {task.recurrence.charAt(0).toUpperCase() + task.recurrence.slice(1)}
            </span>
          </div>
        )}

        {task.tags && task.tags.length > 0 && (
          <div className="info-row">
            <span className="info-label">Tags:</span>
            <span className="info-value">
              {task.tags.map(tag => (
                <span key={tag.id} className="task-tag" style={{ marginRight: '4px' }}>
                  #{tag.name}
                </span>
              ))}
            </span>
          </div>
        )}

        <div className="info-row">
          <span className="info-label">Created:</span>
          <span className="info-value">
            {new Date(task.created_at).toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              year: 'numeric',
              hour: '2-digit',
              minute: '2-digit'
            })}
          </span>
        </div>
      </div>

      {task.subtasks && task.subtasks.length > 0 && (
        <div className="detail-section">
          <div className="detail-section-title">Subtasks ({task.subtasks.length})</div>
          <ul className="subtask-list">
            {task.subtasks.map(subtask => (
              <li key={subtask.id} className="subtask-item">
                <input
                  type="checkbox"
                  className="subtask-checkbox"
                  checked={subtask.is_completed}
                  onChange={() => handleToggleSubtask(subtask.id)}
                />
                <span className={`subtask-title ${subtask.is_completed ? 'completed' : ''}`}>
                  {subtask.title}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {task.attachments && task.attachments.length > 0 && (
        <div className="detail-section">
          <div className="detail-section-title">Attachments ({task.attachments.length})</div>
          <div className="attachments-list">
            {task.attachments.map(attachment => (
              <div key={attachment.id} className="attachment-item">
                {attachment.is_image ? (
                  <div className="attachment-preview">
                    <img src={attachment.file_url} alt={attachment.filename} />
                  </div>
                ) : (
                  <div className="attachment-icon">
                    📎
                  </div>
                )}
                <div className="attachment-info">
                  <div className="attachment-name">{attachment.filename}</div>
                  <div className="attachment-size">{attachment.file_size_formatted}</div>
                </div>
                <div className="attachment-actions">
                  <a href={attachment.file_url} download className="icon-btn-small" title="Download">
                    ⬇️
                  </a>
                  <button
                    className="icon-btn-small danger"
                    onClick={() => handleDeleteAttachment(attachment.id)}
                    title="Delete"
                  >
                    🗑️
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DetailPane;
