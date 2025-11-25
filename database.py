#!/usr/bin/env python3
"""
Database module for Lead Contact Bot
Handles SQLite database operations for storing and retrieving business leads
"""

import sqlite3
from datetime import datetime
import os


class Database:
    """SQLite database handler for business leads"""
    
    def __init__(self, db_path='leads.db'):
        """Initialize database connection and create tables"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                website TEXT,
                category TEXT,
                niche TEXT,
                location TEXT,
                has_website BOOLEAN,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_business(self, name, address, phone, website, category, niche, location):
        """Add a new business to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        has_website = website != 'No website' and website != 'N/A'
        
        cursor.execute('''
            INSERT INTO businesses (name, address, phone, website, category, niche, location, has_website)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, address, phone, website, category, niche, location, has_website))
        
        conn.commit()
        business_id = cursor.lastrowid
        conn.close()
        
        return business_id
    
    def get_all_businesses(self, filter_type='all', search=''):
        """
        Get all businesses with optional filtering
        
        Args:
            filter_type: 'all', 'no_website', or 'has_website'
            search: search term for name or category
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM businesses WHERE 1=1'
        params = []
        
        if filter_type == 'no_website':
            query += ' AND has_website = 0'
        elif filter_type == 'has_website':
            query += ' AND has_website = 1'
        
        if search:
            query += ' AND (name LIKE ? OR category LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += ' ORDER BY date_added DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        businesses = []
        for row in rows:
            businesses.append({
                'id': row['id'],
                'name': row['name'],
                'address': row['address'],
                'phone': row['phone'],
                'website': row['website'],
                'category': row['category'],
                'niche': row['niche'],
                'location': row['location'],
                'has_website': bool(row['has_website']),
                'date_added': row['date_added']
            })
        
        conn.close()
        return businesses
    
    def get_business_by_id(self, business_id):
        """Get a specific business by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM businesses WHERE id = ?', (business_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def delete_business(self, business_id):
        """Delete a business from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM businesses WHERE id = ?', (business_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def clear_all(self):
        """Delete all businesses from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM businesses')
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """Get statistics about stored leads"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total businesses
        cursor.execute('SELECT COUNT(*) FROM businesses')
        total = cursor.fetchone()[0]
        
        # Businesses without website
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE has_website = 0')
        no_website = cursor.fetchone()[0]
        
        # Businesses with website
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE has_website = 1')
        has_website = cursor.fetchone()[0]
        
        # Top categories
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM businesses 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        top_categories = [{'category': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Top niches
        cursor.execute('''
            SELECT niche, COUNT(*) as count 
            FROM businesses 
            GROUP BY niche 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        top_niches = [{'niche': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'total': total,
            'no_website': no_website,
            'has_website': has_website,
            'top_categories': top_categories,
            'top_niches': top_niches
        }
