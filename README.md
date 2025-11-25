# Lead Contact Bot

## Overview

Lead Contact Bot is a Python-based web scraping tool with a modern web interface designed to identify potential business leads for web development services. The program scrapes business directories such as Yellow Pages (Páginas Amarillas), and identifies businesses that either lack an online presence or have websites that could be improved. These leads are stored in a database, classified, and prepared for outreach to offer professional web building services.

## Features

- **🔍 Web Scraping**: Extracts business data from Páginas Amarillas (paginasamarillas.es)
- **💾 Database Storage**: Stores qualified leads in SQLite database
- **📊 Web Dashboard**: Modern, responsive web interface for managing leads
- **🎯 Lead Qualification**: Automatically identifies businesses without websites
- **📈 Real-time Progress**: Live updates during scraping process
- **🔎 Advanced Filtering**: Filter by website status, search by name or category
- **📥 Data Export**: Export leads to JSON format
- **🐳 Docker Support**: Easy deployment with Docker containerization

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

## Manual Installation (Without Docker)

### Prerequisites

- Python 3.11+
- Google Chrome installed

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/sandrosousarivera/lead-contact-bot.git
   cd lead-contact-bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your browser at: **http://localhost:5000**

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
├── app.py                  # Flask web application
├── scraper_module.py       # Web scraping module
├── database.py             # Database operations
├── scraper.py             # Standalone CLI scraper
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose setup
├── start.sh              # Quick start script
├── templates/            # HTML templates
│   └── index.html
├── static/               # Static assets
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
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

## Technologies Used

- **Backend**: Python, Flask
- **Scraping**: Selenium, BeautifulSoup4
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker, Docker Compose

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

This tool is for educational purposes. Always respect websites' Terms of Service and robots.txt files. Use responsibly and ethically.
