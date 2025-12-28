#!/usr/bin/env python
"""
Script to create default categories for the TickTick-style Todo app.
Run this once after migrations to populate your app with starter categories.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_todo_project.settings')
django.setup()

from todo_app.models import Category

# Default categories with nice colors
DEFAULT_CATEGORIES = [
    {'name': 'Inbox', 'color': '#3b82f6'},       # Blue
    {'name': 'Work', 'color': '#ef4444'},        # Red
    {'name': 'Personal', 'color': '#10b981'},    # Green
    {'name': 'Shopping', 'color': '#f59e0b'},    # Orange
    {'name': 'University', 'color': '#8b5cf6'},  # Purple
    {'name': 'Budget', 'color': '#06b6d4'},      # Cyan
    {'name': 'Health', 'color': '#ec4899'},      # Pink
    {'name': 'Projects', 'color': '#14b8a6'},    # Teal
]

def setup_categories():
    """Create default categories if they don't exist."""
    created_count = 0

    for cat_data in DEFAULT_CATEGORIES:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'color': cat_data['color']}
        )

        if created:
            print(f"✓ Created category: {category.name} ({category.color})")
            created_count += 1
        else:
            print(f"- Category already exists: {category.name}")

    print(f"\n{'='*50}")
    print(f"Setup complete! Created {created_count} new categories.")
    print(f"Total categories: {Category.objects.count()}")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Setting up default categories...\n")
    setup_categories()
