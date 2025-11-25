#!/bin/bash

# Lead Contact Bot - Development Stop Script
# This script stops all running dev servers

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Stopping Lead Contact Bot Servers${NC}"
echo -e "${BLUE}============================================${NC}"

# Kill Flask servers
echo -e "${YELLOW}Stopping Flask backend...${NC}"
pkill -f "python3 app.py" || true

# Kill npm dev servers
echo -e "${YELLOW}Stopping npm servers...${NC}"
pkill -f "npm run dev" || true

# Wait a moment
sleep 1

echo ""
echo -e "${GREEN}✅ All servers stopped successfully${NC}"
echo ""
