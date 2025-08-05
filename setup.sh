#!/bin/bash

# Advanced Password Checker Setup Script

echo "🔐 Setting up Advanced Password Checker..."
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 could not be found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if Django is installed
if ! python3 -c "import django" &> /dev/null; then
    echo "📦 Installing Django..."
    pip3 install django
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Django. Please check your pip installation."
        exit 1
    fi
    echo "✅ Django installed successfully"
else
    echo "✅ Django is already installed"
fi

# Run migrations
echo "🗄️  Setting up database..."
python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Database migration failed"
    exit 1
fi
echo "✅ Database setup complete"

# Create sample users
echo "👥 Creating sample users..."
python3 manage.py create_sample_users
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Could not create sample users, but continuing..."
fi

# Check if server can start
echo "🚀 Testing server startup..."
timeout 5s python3 manage.py runserver --noreload > /dev/null 2>&1
if [ $? -eq 124 ]; then
    echo "✅ Server startup test successful"
else
    echo "❌ Server startup test failed"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "  python3 manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000/"
echo ""
echo "Sample accounts:"
echo "  Admin: admin / AdminPassword123!"
echo "  User:  testuser / TestPassword123!"
echo ""
echo "Features:"
echo "  ✨ Real-time password strength checking"
echo "  🧮 Entropy-based password analysis"
echo "  🔍 Pattern and dictionary checking"
echo "  📊 Visual strength indicators"
echo "  🎯 Smart improvement feedback"
echo ""
