#!/bin/bash
# Calorie Tracker Startup Script

echo "🍎 Starting Calorie Tracker..."

# Check if virtual environment exists
if [ ! -d "calorie_env" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv calorie_env

    echo "📦 Installing dependencies..."
    source calorie_env/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo "✅ Dependencies installed successfully!"
else
    echo "✅ Virtual environment found, activating..."
    source calorie_env/bin/activate
fi

# Check if database exists, create if not
if [ ! -f "calorie_tracker.db" ]; then
    echo "🗄️  Creating database..."
    python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created successfully!')"
fi

echo "🚀 Starting Flask development server..."
echo "📱 Open http://localhost:5000 in your browser"
echo "⏹️  Press Ctrl+C to stop"

export FLASK_ENV=development
export FLASK_DEBUG=1

python app.py