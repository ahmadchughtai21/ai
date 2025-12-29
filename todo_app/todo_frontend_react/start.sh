#!/bin/bash

# Start React Frontend for AI Todo App

echo "Starting React Frontend..."
echo "Make sure Django backend is running on http://localhost:8000"
echo ""

cd "$(dirname "$0")"
node_modules/.bin/react-scripts start
