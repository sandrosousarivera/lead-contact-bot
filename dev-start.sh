#!/bin/bash

# Lead Contact Bot - Development Start Script
# This script starts both the React development server and Flask backend

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_DIR="$PROJECT_DIR/frontend"
BACKEND_DIR="$PROJECT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  LEAD CONTACT BOT - Development Server${NC}"
echo -e "${BLUE}============================================${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}❌ Node.js is not installed${NC}"
    echo "Please install Node.js from: https://nodejs.org"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python 3 is not installed${NC}"
    exit 1
fi

# Install frontend dependencies if needed
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    cd "$FRONTEND_DIR"
    npm install
    cd "$BACKEND_DIR"
fi

# Build React frontend
echo -e "${BLUE}🔨 Building React frontend...${NC}"
cd "$FRONTEND_DIR"
npm run build
cd "$BACKEND_DIR"

# Create a temporary script to run both servers
TEMP_SCRIPT=$(mktemp)

cat > "$TEMP_SCRIPT" << 'EOF'
#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_DIR="$PROJECT_DIR/frontend"
BACKEND_DIR="$PROJECT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to handle cleanup on exit
cleanup() {
    echo -e "\n${BLUE}Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    wait $BACKEND_PID 2>/dev/null || true
    echo -e "${GREEN}✅ All servers stopped${NC}"
    rm -f "$TEMP_SCRIPT"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Flask backend
echo -e "${BLUE}🚀 Starting Flask backend...${NC}"
cd "$BACKEND_DIR"
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Display info
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}✅ Development Server is Running${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${BLUE}📱 Open your browser at:${NC}"
echo -e "${GREEN}   http://localhost:5000${NC}"
echo ""
echo -e "${BLUE}📝 To stop the server, press:${NC}"
echo -e "${GREEN}   CTRL + C${NC}"
echo ""

# Keep the script running
wait $BACKEND_PID
EOF

chmod +x "$TEMP_SCRIPT"

# Run the combined server script
bash "$TEMP_SCRIPT"
