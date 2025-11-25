# Lead Contact Bot

## Overview

Lead Contact Bot is a Python-based web scraping tool designed to identify potential business leads for web development services. The program scrapes business directories such as Yellow Pages, verifies business information using Google Maps, and identifies businesses that either lack an online presence or have websites that could be improved. These leads are then stored in a database, classified, and targeted for outreach to offer professional web building services.

## Features

- **Web Scraping**: Extracts business data from online directories like Yellow Pages.
- **Verification**: Cross-checks business details with Google Maps API for accuracy.
- **Lead Qualification**: Identifies businesses without websites or with outdated/improvable online presence.
- **Database Storage**: Stores qualified leads in a structured database.
- **Classification**: Categorizes leads based on industry, location, and potential for web services.
- **Outreach Preparation**: Prepares data for targeted marketing campaigns offering web development solutions.

## Requirements

- Python 3.8+
- Libraries: requests, beautifulsoup4, selenium, googlemaps, sqlite3 (or preferred database)
- Google Maps API key for verification

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/sandrosousarivera/lead-contact-bot.git
   cd lead-contact-bot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Google Maps API key in a `.env` file or environment variables.

## Usage

Run the scraper:
```
python scraper.py
```

The program will scrape specified directories, verify leads, and populate the database.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.