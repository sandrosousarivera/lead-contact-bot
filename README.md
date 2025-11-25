# Lead Contact Bot

## Overview

Lead Contact Bot is a Python-based web scraping tool with a modern React + Tailwind CSS interface designed to identify potential business leads for web development services. The program scrapes business directories such as Yellow Pages (Páginas Amarillas), and identifies businesses that either lack an online presence or have websites that could be improved. These leads are stored in a database, classified, and prepared for outreach to offer professional web building services.

## Features

- **🔍 Web Scraping**: Extracts business data from Páginas Amarillas (paginasamarillas.es)
- **💾 Database Storage**: Stores qualified leads in SQLite database
- **⚛️ React Frontend**: Modern, responsive web interface with React + Tailwind CSS
- **🎯 Lead Qualification**: Automatically identifies businesses without websites
- **📈 Real-time Progress**: Live updates during scraping process
- **🔎 Advanced Filtering**: Filter by website status, search by name or category
- **📥 Data Export**: Export leads to JSON format
- **🐳 Docker Support**: Easy deployment with Docker containerization
- **🎨 Modern UI**: Built with React and Tailwind CSS for beautiful design

## Tech Stack

**Frontend:**

- React 18
- Tailwind CSS
- Axios
- Vite

**Backend:**

- Flask
- SQLite
- Selenium
- BeautifulSoup4

**DevOps:**

- Docker
- Docker Compose

## Quick Start with Docker (Recommended)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/sandrosousarivera/lead-contact-bot.git
   cd lead-contact-bot
   ```

2. Start the application:

   ```bash
   # Make start script executable
   chmod +x start.sh

   # Run the application
   ./start.sh
   ```

   Or manually with docker-compose:

   ```bash
   docker-compose up -d
   ```

3. Open your browser at: **http://localhost:5000**

4. To stop the application:
   ```bash
   docker-compose down
   ```

## Development Setup (Without Docker)

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Chrome installed

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/sandrosousarivera/lead-contact-bot.git
   cd lead-contact-bot
   ```

2. Create virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Build React app:
   ```bash
   npm run build
   ```

### Running the Application

1. In the project root, run Flask:

   ```bash
   python app.py
   ```

2. In another terminal, run React development server (optional):

   ```bash
   cd frontend
   npm run dev
   ```

3. Open your browser at: **http://localhost:5000**

## Usage

### Web Interface

1. **Start a Search**:

   - Enter a business niche (e.g., "restaurantes", "fontaneros", "talleres")
   - Select location (default: España)
   - Choose number of pages to scrape (1-10)
   - Click "Start Scraping"

2. **View Results**:

   - Dashboard shows total leads and those without websites
   - Table displays all business details
   - Filter by website status or search by name/category

3. **Export Data**:
   - Click "Export JSON" to download all leads
   - Use "Clear All" to reset the database

### Command Line (Standalone Scraper)

You can also run the scraper directly:

```bash
python scraper.py
```

## Project Structure

```
lead-contact-bot/
├── app.py                        # Flask backend with API routes
├── scraper_module.py            # Web scraping module
├── database.py                  # SQLite database operations
├── scraper.py                   # Standalone CLI scraper
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image configuration
├── docker-compose.yml           # Docker Compose setup
├── start.sh                     # Quick start script
├── frontend/                    # React frontend (Vite)
│   ├── src/
│   │   ├── main.jsx            # React entry point
│   │   ├── App.jsx             # Main App component
│   │   ├── index.css           # Tailwind styles
│   │   └── components/
│   │       ├── Header.jsx
│   │       ├── StatsGrid.jsx
│   │       ├── SearchForm.jsx
│   │       ├── FilterSection.jsx
│   │       └── ResultsTable.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── static/                      # Compiled React build (auto-generated)
└── README.md
```

## Docker Commands

```bash
# Build the image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Development Commands

### Backend

```bash
# Run Flask development server
python app.py

# Run standalone scraper
python scraper.py
```

### Frontend

```bash
# Install dependencies
npm install

# Run development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Technologies Used

- **Backend**: Python, Flask, Selenium, BeautifulSoup4, SQLite
- **Frontend**: React, Tailwind CSS, Vite, Axios
- **Containerization**: Docker, Docker Compose

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

This tool is for educational purposes. Always respect websites' Terms of Service and robots.txt files. Use responsibly and ethically.
