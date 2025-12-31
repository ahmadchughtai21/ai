import React, { useState, useEffect, useCallback, useRef } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ChatPane from './components/ChatPane';
import TaskListPane from './components/TaskListPane';
import DetailPane from './components/DetailPane';
import TaskForm from './components/TaskForm';
import { ThemeProvider } from './context/ThemeContext';
import {
  getTasks,
  getAllPendingTasks,
  getInboxTasks,
  getTodayTasks,
  getNext7DaysTasks,
  getTasksByCategory,
  getTasksByTag,
  searchTasks,
  getTaskStatistics
} from './services/api';
import './styles/App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [selectedTaskId, setSelectedTaskId] = useState(null);
  const [currentFilter, setCurrentFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTag, setSelectedTag] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [statistics, setStatistics] = useState({});
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const sidebarRef = useRef();
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [mobileChatOpen, setMobileChatOpen] = useState(false);
  const [mobileDetailOpen, setMobileDetailOpen] = useState(false);


  const loadStatistics = useCallback(async () => {
    try {
      const response = await getTaskStatistics();
      setStatistics(response.data);
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  }, []);

  const loadTasks = useCallback(async () => {
    try {
      let response;

      if (searchQuery) {
        response = await searchTasks(searchQuery);
      } else if (selectedTag) {
        response = await getTasksByTag(selectedTag);
      } else if (selectedCategory) {
        response = await getTasksByCategory(selectedCategory);
      } else {
        switch (currentFilter) {
          case 'all':
            response = await getTasks();
            break;
          case 'inbox':
            response = await getInboxTasks();
            break;
          case 'today':
            response = await getTodayTasks();
            break;
          case 'next7days':
            response = await getNext7DaysTasks();
            break;
          default:
            response = await getTasks();
        }
      }

      setTasks(response.data);
      loadStatistics();
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  }, [searchQuery, selectedTag, selectedCategory, currentFilter, loadStatistics]);

  useEffect(() => {
    loadTasks();
  }, [refreshTrigger, loadTasks]);

  const handleFilterChange = (filter) => {
    setCurrentFilter(filter);
    setSelectedTag(null);
    setSelectedCategory(null);
    setSearchQuery('');

    // Load tasks with new filter
    setTimeout(() => {
      loadTasksByFilter(filter);
    }, 0);
  };

  const loadTasksByFilter = async (filter) => {
    try {
      let response;
      switch (filter) {
        case 'all':
          response = await getAllPendingTasks();
          break;
        case 'inbox':
          response = await getInboxTasks();
          break;
        case 'today':
          response = await getTodayTasks();
          break;
        case 'next7days':
          response = await getNext7DaysTasks();
          break;
        default:
          response = await getTasks();
      }
      setTasks(response.data);
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  const handleSearch = async (query) => {
    setSearchQuery(query);
    if (query) {
      try {
        const response = await searchTasks(query);
        setTasks(response.data);
      } catch (error) {
        console.error('Error searching tasks:', error);
      }
    } else {
      loadTasks();
    }
  };

  const handleCategoryFilter = async (categoryName) => {
    setCurrentFilter('category-' + categoryName);
    setSelectedCategory(categoryName);
    setSelectedTag(null);
    setSearchQuery('');

    try {
      const response = await getTasksByCategory(categoryName);
      setTasks(response.data);
    } catch (error) {
      console.error('Error filtering by category:', error);
    }
  };

  const handleTagFilter = (tagName) => {
    setSelectedTag(tagName);
    setCurrentFilter(tagName ? 'tag-' + tagName : 'all');
    setSelectedCategory(null);
    setSearchQuery('');
  };

  const handleTaskSelect = (taskId) => {
    setSelectedTaskId(taskId);
    // Auto-open detail pane on mobile when task is selected
    if (window.innerWidth <= 1024) {
      setMobileDetailOpen(true);
    }
  };

  const handleTaskDeleted = () => {
    setSelectedTaskId(null);
    setRefreshTrigger(prev => prev + 1);
  };

  const handleTasksUpdated = useCallback(() => {
    console.log('Tasks updated, refreshing...');
    setRefreshTrigger(prev => prev + 1);
    // Also trigger sidebar to reload categories and tags
    if (sidebarRef.current?.reloadData) {
      sidebarRef.current.reloadData();
    }
  }, []);

  const handleAddTask = () => {
    setEditingTask(null);
    setShowTaskForm(true);
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleFormSave = () => {
    setShowTaskForm(false);
    setEditingTask(null);
    handleTasksUpdated();
  };

  const handleFormCancel = () => {
    setShowTaskForm(false);
    setEditingTask(null);
  };

  const toggleMobileSidebar = () => {
    setMobileSidebarOpen(!mobileSidebarOpen);
    setMobileChatOpen(false);
    setMobileDetailOpen(false);
  };

  const toggleMobileChat = () => {
    setMobileChatOpen(!mobileChatOpen);
    setMobileSidebarOpen(false);
    setMobileDetailOpen(false);
  };

  const closeMobileMenus = () => {
    setMobileSidebarOpen(false);
    setMobileChatOpen(false);
    setMobileDetailOpen(false);
  };

  const closeMobileDetail = () => {
    setMobileDetailOpen(false);
  };

  return (
    <ThemeProvider>
      <div className="app-container">
        <Navbar
          onAddTask={handleAddTask}
          onToggleSidebar={toggleMobileSidebar}
          onToggleChat={toggleMobileChat}
        />
        <Sidebar
          ref={sidebarRef}
          onFilterChange={handleFilterChange}
          onSearch={handleSearch}
          onCategoryFilter={handleCategoryFilter}
          onTagFilter={handleTagFilter}
          currentFilter={currentFilter}
          statistics={statistics}
          selectedTag={selectedTag}
          className={mobileSidebarOpen ? 'mobile-visible' : ''}
          onMobileClose={closeMobileMenus}
        />
        <ChatPane
          onTasksUpdated={handleTasksUpdated}
          className={mobileChatOpen ? 'mobile-visible' : ''}
        />
        <TaskListPane
          tasks={tasks}
          onTaskSelect={handleTaskSelect}
          selectedTaskId={selectedTaskId}
          onTaskToggle={handleTasksUpdated}
          onSearch={handleSearch}
        />
        <DetailPane
          taskId={selectedTaskId}
          onTaskDeleted={handleTaskDeleted}
          onTaskUpdated={handleTasksUpdated}
          onEditTask={handleEditTask}
          refreshTrigger={refreshTrigger}
          className={mobileDetailOpen ? 'mobile-visible' : ''}
          onClose={closeMobileDetail}
        />
        {showTaskForm && (
          <TaskForm
            task={editingTask}
            onSave={handleFormSave}
            onCancel={handleFormCancel}
          />
        )}
        {/* Mobile overlay */}
        <div
          className={`mobile-overlay ${mobileSidebarOpen || mobileChatOpen || mobileDetailOpen ? 'active' : ''}`}
          onClick={closeMobileMenus}
        ></div>
      </div>
    </ThemeProvider>
  );
}

export default App;
