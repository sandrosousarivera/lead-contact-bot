#!/bin/bash

echo "🚀 Starting Lead Contact Bot with Docker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker is installed"
echo ""

# Build and start containers
echo "📦 Building Docker image..."
docker-compose build

echo ""
echo "🎬 Starting container..."
docker-compose up -d

echo ""
echo "✅ Lead Contact Bot is running!"
echo ""
echo "📱 Open your browser at: http://localhost:5000"
echo ""
echo "To stop the application, run:"
echo "   docker-compose down"
echo ""
echo "To view logs, run:"
echo "   docker-compose logs -f"
