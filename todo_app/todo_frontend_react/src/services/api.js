import axios from 'axios';

// Use relative URL to leverage the proxy configuration in package.json
const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401 && typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('auth:unauthorized'));
    }
    return Promise.reject(error);
  }
);

const setCsrfHeader = (token) => {
  if (!token) return;
  api.defaults.headers.common['X-CSRFToken'] = token;
};

const getCookie = (name) => {
  if (typeof document === 'undefined') return null;
  const cookieValue = document.cookie
    .split('; ')
    .find((row) => row.startsWith(`${name}=`))
    ?.split('=')[1];
  return cookieValue || null;
};

api.interceptors.request.use((config) => {
  const method = (config.method || 'get').toLowerCase();
  const unsafeMethod = ['post', 'put', 'patch', 'delete'].includes(method);
  if (unsafeMethod) {
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
      config.headers = config.headers || {};
      config.headers['X-CSRFToken'] = csrfToken;
    }
  }
  return config;
});

// Auth
export const getCsrfToken = async () => {
  const response = await axios.get('/api/auth/csrf/', { withCredentials: true });
  const token = response.data?.csrfToken;
  setCsrfHeader(token);
  return token;
};
export const getAuthStatus = () => api.get('/auth/status/');
export const signup = (username, password1, password2) =>
  api.post('/auth/signup/', { username, password1, password2 });
export const login = (username, password) =>
  api.post('/auth/login/', { username, password });
export const logout = () => api.post('/auth/logout/');

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
