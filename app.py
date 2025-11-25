#!/usr/bin/env python3
"""
Flask Web Application for Lead Contact Bot
Provides web interface for scraping and managing business leads
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import threading
import json
import os
from pathlib import Path
from datetime import datetime
from scraper_module import PaginasAmarillasScraper
from database import Database

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Global variables
scraping_status = {
    'is_running': False,
    'current_page': 0,
    'total_businesses': 0,
    'progress': 0,
    'message': ''
}

db = Database()


@app.route('/')
@app.route('/<path:path>')
def serve_react(path='index.html'):
    """Serve React application"""
    static_dir = Path(__file__).parent / 'static'
    
    # If requesting a specific file that exists, serve it
    if path != 'index.html':
        file_path = static_dir / path
        if file_path.exists() and file_path.is_file():
            return send_from_directory('static', path)
    
    # Otherwise serve index.html for React SPA routing
    return send_from_directory('static', 'index.html')


@app.route('/api/start-scraping', methods=['POST'])
def start_scraping():
    """Start scraping process in background thread"""
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({'error': 'Scraping already in progress'}), 400
    
    data = request.json
    niche = data.get('niche', '')
    location = data.get('location', 'España')
    max_pages = int(data.get('max_pages', 3))
    
    if not niche:
        return jsonify({'error': 'Niche is required'}), 400
    
    # Reset status
    scraping_status = {
        'is_running': True,
        'current_page': 0,
        'total_businesses': 0,
        'progress': 0,
        'message': f'Starting scrape for {niche}...'
    }
    
    # Start scraping in background thread
    thread = threading.Thread(
        target=run_scraper,
        args=(niche, location, max_pages)
    )
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Scraping started successfully'})


def run_scraper(niche, location, max_pages):
    """Run scraper in background and update status"""
    global scraping_status
    
    try:
        scraper = PaginasAmarillasScraper()
        scraper.setup_driver()
        
        # Custom callback to update status
        def update_callback(page, total):
            scraping_status['current_page'] = page
            scraping_status['total_businesses'] = total
            scraping_status['progress'] = int((page / max_pages) * 100)
            scraping_status['message'] = f'Scraping page {page}/{max_pages}... ({total} businesses found)'
        
        # Run scraper
        businesses = scraper.search_niche(niche, location, max_pages, callback=update_callback)
        
        # Save to database
        for business in businesses:
            db.add_business(
                name=business['name'],
                address=business['address'],
                phone=business['phone'],
                website=business['website'],
                category=business['category'],
                niche=niche,
                location=location
            )
        
        scraper.close()
        
        scraping_status['is_running'] = False
        scraping_status['progress'] = 100
        scraping_status['message'] = f'Completed! Found {len(businesses)} businesses'
        
    except Exception as e:
        scraping_status['is_running'] = False
        scraping_status['message'] = f'Error: {str(e)}'


@app.route('/api/status')
def get_status():
    """Get current scraping status"""
    return jsonify(scraping_status)


@app.route('/api/leads')
def get_leads():
    """Get all leads from database"""
    filter_type = request.args.get('filter', 'all')
    search = request.args.get('search', '')
    
    leads = db.get_all_businesses(filter_type=filter_type, search=search)
    return jsonify(leads)


@app.route('/api/stats')
def get_stats():
    """Get statistics about leads"""
    stats = db.get_statistics()
    return jsonify(stats)


@app.route('/api/export')
def export_leads():
    """Export leads to JSON file"""
    leads = db.get_all_businesses()
    
    filename = f'leads_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    filepath = os.path.join('exports', filename)
    
    os.makedirs('exports', exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    
    return send_file(filepath, as_attachment=True, download_name=filename)


@app.route('/api/delete-lead/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    """Delete a specific lead"""
    success = db.delete_business(lead_id)
    if success:
        return jsonify({'message': 'Lead deleted successfully'})
    return jsonify({'error': 'Lead not found'}), 404


@app.route('/api/clear-all', methods=['POST'])
def clear_all():
    """Clear all leads from database"""
    db.clear_all()
    return jsonify({'message': 'All leads cleared successfully'})


if __name__ == '__main__':
    print("=" * 60)
    print("  LEAD CONTACT BOT - Web Interface")
    print("=" * 60)
    print("\n🚀 Starting server...")
    print("📱 Open your browser at: http://localhost:5000")
    print("🛑 Press CTRL+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
