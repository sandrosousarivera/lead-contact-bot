#!/bin/bash

# Lead Contact Bot - Quick Setup and Start
# One-command setup: installs all dependencies and starts the dev server

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_DIR="$PROJECT_DIR/frontend"
BACKEND_DIR="$PROJECT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  LEAD CONTACT BOT - Setup & Start${NC}"
echo -e "${BLUE}============================================${NC}"

# Check dependencies
echo -e "${BLUE}Checking dependencies...${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found${NC}"
    echo "Install from: https://nodejs.org"
    exit 1
fi
echo -e "${GREEN}✓ Node.js${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3${NC}"

# Setup backend
echo -e "${BLUE}Setting up backend...${NC}"
cd "$BACKEND_DIR"

if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
fi

# Check if virtual environment exists, create if not
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate venv and install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
source venv/bin/activate
pip install -q -r requirements.txt
deactivate

# Setup frontend
echo -e "${BLUE}Setting up frontend...${NC}"
cd "$FRONTEND_DIR"

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${YELLOW}Installing npm dependencies...${NC}"
    npm install -q
fi

echo -e "${YELLOW}Building React app...${NC}"
npm run build -q

# All set!
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${BLUE}To start the development server, run:${NC}"
echo -e "${YELLOW}./dev-start.sh${NC}"
echo ""
echo -e "${BLUE}To stop the servers, run:${NC}"
echo -e "${YELLOW}./dev-stop.sh${NC}"
echo ""
