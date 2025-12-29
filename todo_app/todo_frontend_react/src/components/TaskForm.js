import React, { useState, useEffect } from 'react';
import { createTask, updateTask, getCategories, uploadAttachment } from '../services/api';

const TaskForm = ({ task, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'none',
    category: '',
    due_date_only: '',
    due_time: '',
    status: 'pending',
    recurrence: 'none'
  });
  const [categories, setCategories] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [subtasks, setSubtasks] = useState([]);
  const [newSubtaskText, setNewSubtaskText] = useState('');

  useEffect(() => {
    loadCategories();
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        priority: task.priority || 'none',
        category: task.category || '',
        due_date_only: task.due_date_only || '',
        due_time: task.due_time || '',
        status: task.status || 'pending',
        recurrence: task.recurrence || 'none'
      });
      // Load existing subtasks
      if (task.subtasks && task.subtasks.length > 0) {
        setSubtasks(task.subtasks.map(st => st.title));
      }
    }
  }, [task]);

  const loadCategories = async () => {
    try {
      const response = await getCategories();
      setCategories(response.data);
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setUploading(true);

    try {
      let taskId;
      const taskData = { ...formData };

      // Add subtasks if any
      if (subtasks.length > 0) {
        taskData.subtasks = subtasks;
      }

      if (task) {
        await updateTask(task.id, taskData);
        taskId = task.id;
      } else {
        const response = await createTask(taskData);
        taskId = response.data.id;
      }

      // Upload attachments if any
      if (selectedFiles.length > 0) {
        for (const file of selectedFiles) {
          await uploadAttachment(taskId, file);
        }
      }

      onSave();
    } catch (error) {
      console.error('Error saving task:', error);
      alert('Failed to save task');
    } finally {
      setUploading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(prev => [...prev, ...files]);
  };

  const removeSelectedFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const addSubtask = () => {
    if (newSubtaskText.trim()) {
      setSubtasks(prev => [...prev, newSubtaskText.trim()]);
      setNewSubtaskText('');
    }
  };

  const removeSubtask = (index) => {
    setSubtasks(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubtaskKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addSubtask();
    }
  };

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{task ? 'Edit Task' : 'New Task'}</h2>
          <button className="modal-close" onClick={onCancel}>×</button>
        </div>
        <form onSubmit={handleSubmit} className="task-form">
          <div className="form-group">
            <label>Title *</label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Task title"
              required
              autoFocus
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Add details..."
              rows="3"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Priority</label>
              <select name="priority" value={formData.priority} onChange={handleChange}>
                <option value="none">None</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div className="form-group">
              <label>Category</label>
              <select name="category" value={formData.category} onChange={handleChange}>
                <option value="">Inbox</option>
                {categories.map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>
                {formData.recurrence === 'monthly' ? 'Day of Month' :
                 formData.recurrence === 'yearly' ? 'Date (Month & Day)' :
                 formData.recurrence === 'weekly' ? 'Starting Date' :
                 formData.recurrence === 'daily' ? 'Starting Date' : 'Due Date'}
              </label>
              {formData.recurrence === 'monthly' ? (
                <select
                  name="due_date_day"
                  value={formData.due_date_only ? new Date(formData.due_date_only).getDate() : ''}
                  onChange={(e) => {
                    const today = new Date();
                    const day = parseInt(e.target.value);
                    if (day) {
                      // Start with current month
                      let newDate = new Date(today.getFullYear(), today.getMonth(), day);
                      // If the date has already passed this month, use next month
                      if (newDate < today) {
                        newDate = new Date(today.getFullYear(), today.getMonth() + 1, day);
                      }
                      setFormData(prev => ({ ...prev, due_date_only: newDate.toISOString().split('T')[0] }));
                    } else {
                      setFormData(prev => ({ ...prev, due_date_only: '' }));
                    }
                  }}
                >
                  <option value="">Select day...</option>
                  {Array.from({ length: 31 }, (_, i) => i + 1).map(day => (
                    <option key={day} value={day}>{day}</option>
                  ))}
                </select>
              ) : (
                <input
                  type="date"
                  name="due_date_only"
                  value={formData.due_date_only}
                  onChange={handleChange}
                />
              )}
              {formData.recurrence === 'monthly' && formData.due_date_only && (
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
                  Repeats on day {new Date(formData.due_date_only).getDate()} every month
                </div>
              )}
              {formData.recurrence === 'yearly' && formData.due_date_only && (
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
                  Repeats on {new Date(formData.due_date_only + 'T00:00:00').toLocaleDateString('en-US', { month: 'long', day: 'numeric' })} every year
                </div>
              )}
            </div>

            <div className="form-group">
              <label>Time</label>
              <input
                type="time"
                name="due_time"
                value={formData.due_time}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Repeat</label>
            <select name="recurrence" value={formData.recurrence} onChange={handleChange}>
              <option value="none">Don't repeat</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
              <option value="yearly">Yearly</option>
            </select>
            {formData.recurrence !== 'none' && (
              <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '6px' }}>
                🔁 When you complete this task, a new occurrence will be created automatically
              </div>
            )}
          </div>

          <div className="form-group">
            <label>Attachments</label>
            <input
              type="file"
              multiple
              onChange={handleFileSelect}
              accept="image/*,application/pdf,.doc,.docx,.txt"
            />
            {selectedFiles.length > 0 && (
              <div className="selected-files">
                {selectedFiles.map((file, index) => (
                  <div key={index} className="selected-file-item">
                    <span>{file.name}</span>
                    <button
                      type="button"
                      className="remove-file-btn"
                      onClick={() => removeSelectedFile(index)}
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="form-group">
            <label>Checklist Items</label>
            <div className="subtask-input-row">
              <input
                type="text"
                value={newSubtaskText}
                onChange={(e) => setNewSubtaskText(e.target.value)}
                onKeyPress={handleSubtaskKeyPress}
                placeholder="Add checklist item..."
              />
              <button
                type="button"
                className="btn-add-subtask"
                onClick={addSubtask}
                disabled={!newSubtaskText.trim()}
              >
                + Add
              </button>
            </div>
            {subtasks.length > 0 && (
              <div className="subtasks-list">
                {subtasks.map((subtask, index) => (
                  <div key={index} className="subtask-item">
                    <span>☐ {subtask}</span>
                    <button
                      type="button"
                      className="remove-subtask-btn"
                      onClick={() => removeSubtask(index)}
                      title="Remove item"
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={onCancel} disabled={uploading}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={uploading}>
              {uploading ? 'Uploading...' : (task ? 'Save Changes' : 'Create Task')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TaskForm;
