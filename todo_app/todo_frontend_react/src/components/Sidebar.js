import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { getCategories, getPendingTasksTags } from '../services/api';
import CategoryManager from './CategoryManager';

const Sidebar = forwardRef(({
  onFilterChange,
  onSearch,
  onCategoryFilter,
  onTagFilter,
  currentFilter,
  statistics,
  selectedTag,
  className = '',
  onMobileClose
}, ref) => {
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);
  const [showCategoryManager, setShowCategoryManager] = useState(false);

  useEffect(() => {
    loadCategories();
    loadTags();
  }, []);

  // Expose reload methods to parent via ref
  useImperativeHandle(ref, () => ({
    reloadData: () => {
      loadCategories();
      loadTags();
    }
  }));

  const loadCategories = async () => {
    try {
      const response = await getCategories();
      setCategories(response.data);
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  };

  const loadTags = async () => {
    try {
      const response = await getPendingTasksTags();
      setTags(response.data);
    } catch (error) {
      console.error('Error loading tags:', error);
    }
  };

  const handleTagClick = (tagName) => {
    const newTag = selectedTag === tagName ? null : tagName;
    onTagFilter(newTag);
    if (onMobileClose && window.innerWidth <= 480) {
      onMobileClose();
    }
  };

  return (
    <div className={`sidebar ${className}`}>
      <div className="sidebar-section">
        <div className="sidebar-title">Smart Views</div>
        <div
          className={`sidebar-item ${currentFilter === 'all' ? 'active' : ''}`}
          onClick={() => {
            onFilterChange('all');
            if (onMobileClose && window.innerWidth <= 480) onMobileClose();
          }}
        >
          <span className="icon">📋</span>
          <span>All</span>
          <span className="count" id="all-count">{statistics?.pending || 0}</span>
        </div>
        <div
          className={`sidebar-item ${currentFilter === 'inbox' ? 'active' : ''}`}
          onClick={() => {
            onFilterChange('inbox');
            if (onMobileClose && window.innerWidth <= 480) onMobileClose();
          }}
        >
          <span className="icon">📥</span>
          <span>Inbox</span>
          <span className="count" id="inbox-count">{statistics?.inbox || 0}</span>
        </div>
        <div
          className={`sidebar-item ${currentFilter === 'today' ? 'active' : ''}`}
          onClick={() => {
            onFilterChange('today');
            if (onMobileClose && window.innerWidth <= 480) onMobileClose();
          }}
        >
          <span className="icon">📅</span>
          <span>Today</span>
          <span className="count" id="today-count">{statistics?.today || 0}</span>
        </div>
        <div
          className={`sidebar-item ${currentFilter === 'next7days' ? 'active' : ''}`}
          onClick={() => {
            onFilterChange('next7days');
            if (onMobileClose && window.innerWidth <= 480) onMobileClose();
          }}
        >
          <span className="icon">🗓️</span>
          <span>Next 7 Days</span>
          <span className="count" id="week-count">{statistics?.next_7_days || 0}</span>
        </div>
      </div>

      <div className="sidebar-section">
        <div className="section-header">
          <div className="sidebar-title">Categories</div>
          <button
            className="category-settings-btn"
            onClick={() => setShowCategoryManager(true)}
            title="Manage Categories"
          >
            ⚙️
          </button>
        </div>
        <div id="categories-list">
          {categories.map(category => (
            <div
              key={category.id}
              className={`sidebar-item ${currentFilter === 'category-' + category.name ? 'active' : ''}`}
              onClick={() => {
                onCategoryFilter(category.name);
                if (onMobileClose && window.innerWidth <= 480) onMobileClose();
              }}
            >
              <span
                className="category-color"
                style={{ backgroundColor: category.color }}
              ></span>
              <span>{category.name}</span>
              <span className="count">{category.task_count || 0}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="sidebar-section">
        <div className="sidebar-title">Tags</div>
        <div id="tags-list">
          {tags.length === 0 ? (
            <div style={{ padding: '10px 20px', fontSize: '13px', color: 'var(--text-muted)' }}>
              No tags yet
            </div>
          ) : (
            tags.map(tag => (
              <div
                key={tag.id}
                className={`tag-item ${selectedTag === tag.name ? 'active' : ''}`}
                onClick={() => handleTagClick(tag.name)}
              >
                <span className="icon">#</span>
                <span>{tag.name}</span>
                <span className="count">{tag.task_count || 0}</span>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Category Manager Modal */}
      {showCategoryManager && (
        <CategoryManager
          onClose={() => setShowCategoryManager(false)}
          onCategoryUpdated={() => {
            loadCategories();
            // Optionally reload tasks if needed
          }}
          categories={categories}
        />
      )}
    </div>
  );
});

export default Sidebar;
