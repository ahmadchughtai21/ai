import React, { useState } from 'react';
import { createCategory, updateCategory, deleteCategory } from '../services/api';

const CategoryManager = ({ onClose, onCategoryUpdated, categories }) => {
  const [categoryName, setCategoryName] = useState('');
  const [categoryColor, setCategoryColor] = useState('#3b82f6');
  const [isCreating, setIsCreating] = useState(false);

  const handleCreateCategory = async (e) => {
    e.preventDefault();
    if (!categoryName.trim()) return;

    try {
      await createCategory({ name: categoryName, color: categoryColor });
      setCategoryName('');
      setCategoryColor('#3b82f6');
      setIsCreating(false);
      onCategoryUpdated();
    } catch (error) {
      console.error('Error creating category:', error);
      alert('Failed to create category');
    }
  };

  const handleUpdateCategory = async (category) => {
    const newName = prompt('Enter new category name:', category.name);
    if (!newName || newName === category.name) return;

    try {
      await updateCategory(category.id, { name: newName });
      onCategoryUpdated();
    } catch (error) {
      console.error('Error updating category:', error);
      alert('Failed to update category');
    }
  };

  const handleChangeColor = async (category) => {
    const newColor = prompt('Enter new color (hex code):', category.color);
    if (!newColor || newColor === category.color) return;

    try {
      await updateCategory(category.id, { color: newColor });
      onCategoryUpdated();
    } catch (error) {
      console.error('Error updating category color:', error);
      alert('Failed to update category color');
    }
  };

  const handleDeleteCategory = async (category) => {
    if (category.name === 'Inbox') {
      alert('Cannot delete Inbox category');
      return;
    }

    if (!window.confirm(`Delete "${category.name}"? All tasks will be moved to Inbox.`)) {
      return;
    }

    try {
      await deleteCategory(category.id);
      onCategoryUpdated();
    } catch (error) {
      console.error('Error deleting category:', error);
      alert('Failed to delete category');
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content category-manager-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Manage Categories</h2>
          <button
            className="modal-close-btn"
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#ff4444',
              fontSize: '24px',
              cursor: 'pointer',
              padding: '4px 8px',
              lineHeight: 1,
              transition: 'opacity 0.2s ease'
            }}
            onMouseEnter={(e) => e.target.style.opacity = '0.7'}
            onMouseLeave={(e) => e.target.style.opacity = '1'}
          >
            ✕
          </button>
        </div>

        <div className="modal-body">
          {/* Create New Category Section */}
          {!isCreating ? (
            <button
              className="btn-primary"
              onClick={() => setIsCreating(true)}
              style={{ marginBottom: '20px', width: '100%' }}
            >
              + New Category
            </button>
          ) : (
            <form onSubmit={handleCreateCategory} className="category-form" style={{ marginBottom: '20px' }}>
              <div className="form-group">
                <input
                  type="text"
                  className="form-input"
                  placeholder="Category name..."
                  value={categoryName}
                  onChange={(e) => setCategoryName(e.target.value)}
                  autoFocus
                />
              </div>
              <div className="form-group">
                <label>Color:</label>
                <input
                  type="color"
                  value={categoryColor}
                  onChange={(e) => setCategoryColor(e.target.value)}
                  style={{ width: '100%', height: '40px', border: '1px solid var(--border-color)', borderRadius: '8px' }}
                />
              </div>
              <div style={{ display: 'flex', gap: '10px' }}>
                <button type="submit" className="btn-primary">Create</button>
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => {
                    setIsCreating(false);
                    setCategoryName('');
                    setCategoryColor('#3b82f6');
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          {/* Category List */}
          <div className="category-list">
            <h3 style={{ marginBottom: '12px', fontSize: '14px', color: 'var(--text-muted)', paddingLeft: '0' }}>
              EXISTING CATEGORIES
            </h3>
            {categories.map(category => (
              <div key={category.id} className="category-manager-item">
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flex: 1 }}>
                  <span
                    className="category-color"
                    style={{
                      backgroundColor: category.color,
                      width: '20px',
                      height: '20px',
                      borderRadius: '4px',
                      display: 'inline-block'
                    }}
                  ></span>
                  <span style={{ flex: 1 }}>{category.name}</span>
                  <span style={{ color: 'var(--text-muted)', fontSize: '12px', padding: '0px 5px' }}>
                    {category.task_count || 0} tasks
                  </span>
                </div>
                <div className="category-actions">
                  <button
                    className="icon-btn-small"
                    onClick={() => handleChangeColor(category)}
                    title="Change color"
                  >
                    🎨
                  </button>
                  <button
                    className="icon-btn-small"
                    onClick={() => handleUpdateCategory(category)}
                    title="Rename"
                  >
                    ✏️
                  </button>
                  {category.name !== 'Inbox' ? (
                    <button
                      className="icon-btn-small danger"
                      onClick={() => handleDeleteCategory(category)}
                      title="Delete"
                    >
                      🗑️
                    </button>
                  ) : (
                    <button
                      className="icon-btn-small"
                      style={{ visibility: 'hidden' }}
                      disabled
                    >
                      🗑️
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CategoryManager;
