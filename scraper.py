#!/usr/bin/env python3
"""
Paginas Amarillas Scraper
Scrapes business information from paginasamarillas.es based on user-specified niche/category
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import json
from urllib.parse import quote


class PaginasAmarillasScraper:
    """Scraper for extracting business data from Paginas Amarillas"""
    
    def __init__(self):
        """Initialize the scraper with Chrome WebDriver"""
        self.base_url = "https://www.paginasamarillas.es"
        self.driver = None
        self.businesses = []
        
    def setup_driver(self):
        """Configure and initialize Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✓ Chrome WebDriver initialized")
        
    def search_niche(self, niche, location="España", max_pages=3):
        """
        Search for businesses in a specific niche
        
        Args:
            niche (str): Business category or niche to search for
            location (str): Location to search in (default: España)
            max_pages (int): Maximum number of pages to scrape
        """
        print(f"\n🔍 Searching for '{niche}' in '{location}'...")
        
        # Construct search URL
        search_url = f"{self.base_url}/buscar/{quote(niche)}/{quote(location)}"
        
        try:
            self.driver.get(search_url)
            time.sleep(3)  # Wait for page to load
            
            for page in range(1, max_pages + 1):
                print(f"\n📄 Scraping page {page}...")
                self._scrape_current_page()
                
                # Try to go to next page
                if page < max_pages:
                    if not self._go_to_next_page():
                        print("No more pages available")
                        break
                    time.sleep(2)
            
            print(f"\n✓ Scraping complete! Found {len(self.businesses)} businesses")
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            
    def _scrape_current_page(self):
        """Extract business information from the current page"""
        try:
            # Wait for business listings to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "listado-resultado"))
            )
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            listings = soup.find_all('article', class_='resultado')
            
            for listing in listings:
                business = self._extract_business_info(listing)
                if business:
                    self.businesses.append(business)
                    print(f"  ✓ {business['name']}")
                    
        except Exception as e:
            print(f"  ⚠️ Error extracting data from page: {e}")
            
    def _extract_business_info(self, listing):
        """
        Extract detailed information from a business listing
        
        Args:
            listing: BeautifulSoup element containing business data
            
        Returns:
            dict: Business information
        """
        try:
            business = {}
            
            # Business name
            name_elem = listing.find('h2', class_='nombre')
            business['name'] = name_elem.get_text(strip=True) if name_elem else 'N/A'
            
            # Address
            address_elem = listing.find('p', class_='direccion')
            business['address'] = address_elem.get_text(strip=True) if address_elem else 'N/A'
            
            # Phone number
            phone_elem = listing.find('span', class_='telefono')
            business['phone'] = phone_elem.get_text(strip=True) if phone_elem else 'N/A'
            
            # Website
            website_elem = listing.find('a', class_='web')
            business['website'] = website_elem['href'] if website_elem and website_elem.get('href') else 'No website'
            
            # Category
            category_elem = listing.find('p', class_='actividad')
            business['category'] = category_elem.get_text(strip=True) if category_elem else 'N/A'
            
            return business
            
        except Exception as e:
            print(f"  ⚠️ Error extracting business info: {e}")
            return None
            
    def _go_to_next_page(self):
        """Navigate to the next page of results"""
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, 'a.siguiente')
            if next_button and next_button.is_enabled():
                next_button.click()
                return True
            return False
        except:
            return False
            
    def save_results(self, filename='businesses.json'):
        """Save scraped businesses to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.businesses, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Results saved to {filename}")
        
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            print("\n✓ Browser closed")


def main():
    """Main execution function"""
    print("=" * 60)
    print("  PAGINAS AMARILLAS SCRAPER")
    print("=" * 60)
    
    # Get user input
    niche = input("\n📋 Enter the business niche/category to search: ").strip()
    location = input("📍 Enter location (press Enter for 'España'): ").strip() or "España"
    
    try:
        max_pages = int(input("📄 How many pages to scrape? (1-10): ").strip() or "3")
        max_pages = min(max(1, max_pages), 10)  # Limit between 1-10
    except:
        max_pages = 3
        
    # Initialize and run scraper
    scraper = PaginasAmarillasScraper()
    
    try:
        scraper.setup_driver()
        scraper.search_niche(niche, location, max_pages)
        scraper.save_results()
        
        # Display summary
        print("\n" + "=" * 60)
        print(f"  SUMMARY: {len(scraper.businesses)} businesses found")
        print("=" * 60)
        
        # Show businesses without website
        no_website = [b for b in scraper.businesses if b.get('website') == 'No website']
        print(f"\n🎯 Businesses without website: {len(no_website)}")
        
        if no_website:
            print("\nTop 5 leads without website:")
            for business in no_website[:5]:
                print(f"  • {business['name']} - {business['phone']}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
