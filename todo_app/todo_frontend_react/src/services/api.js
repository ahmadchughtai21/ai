import axios from 'axios';

// Use relative URL to leverage the proxy configuration in package.json
const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Tasks
export const getTasks = () => api.get('/tasks/');
export const getAllPendingTasks = () => api.get('/tasks/all_pending/');
export const getInboxTasks = () => api.get('/tasks/inbox/');
export const getTodayTasks = () => api.get('/tasks/today/');
export const getNext7DaysTasks = () => api.get('/tasks/next7days/');
export const getTasksByCategory = (category) => api.get(`/tasks/by_category/?category=${encodeURIComponent(category)}`);
export const getTasksByTag = (tag) => api.get(`/tasks/by_tag/?tag=${encodeURIComponent(tag)}`);
export const searchTasks = (query) => api.get(`/tasks/search/?q=${encodeURIComponent(query)}`);
export const getTaskStatistics = () => api.get('/tasks/statistics/');
export const createTask = (taskData) => api.post('/tasks/', taskData);
export const getTask = (id) => api.get(`/tasks/${id}/`);
export const updateTask = (id, taskData) => api.patch(`/tasks/${id}/`, taskData);
export const deleteTask = (id) => api.delete(`/tasks/${id}/`);
export const addSubtask = (taskId, subtaskData) => api.post(`/tasks/${taskId}/add_subtask/`, subtaskData);

// Categories
export const getCategories = () => api.get('/categories/');
export const createCategory = (categoryData) => api.post('/categories/', categoryData);
export const updateCategory = (id, categoryData) => api.patch(`/categories/${id}/`, categoryData);
export const deleteCategory = (id) => api.delete(`/categories/${id}/`);

// Tags
export const getTags = () => api.get('/tags/');
export const getPendingTasksTags = () => api.get('/tags/pending_tasks_tags/');
export const createTag = (tagData) => api.post('/tags/', tagData);

// Subtasks
export const getSubtasks = () => api.get('/subtasks/');
export const createSubtask = (subtaskData) => api.post('/subtasks/', subtaskData);
export const toggleSubtaskComplete = (id) => api.patch(`/subtasks/${id}/toggle_complete/`);
export const updateSubtask = (id, subtaskData) => api.patch(`/subtasks/${id}/`, subtaskData);
export const deleteSubtask = (id) => api.delete(`/subtasks/${id}/`);

// Chat
export const sendChatMessage = (message) => api.post('/chat/', { message });
export const getChatHistory = () => api.get('/chat/history/');
export const clearChatHistory = () => api.post('/chat/clear/');

// Attachments
export const uploadAttachment = (taskId, file) => {
  const formData = new FormData();
  formData.append('task', taskId);
  formData.append('file', file);

  return api.post('/attachments/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};
export const deleteAttachment = (id) => api.delete(`/attachments/${id}/`);

export default api;
