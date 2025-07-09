import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import os
# These imports are for Selenium, which is currently commented out for simplicity in this agent integration.
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# Define a browser-like User-Agent header for all requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Define a temporary storage directory for unprocessed HTML files
# This is mainly for local testing/debugging if needed, the agent will process in-memory.
TEMP_UNPROCESSED_DIR = 'temp_unprocessed_html'
if not os.path.exists(TEMP_UNPROCESSED_DIR):
    os.makedirs(TEMP_UNPROCESSED_DIR)

def check_robots_txt(url):
    """
    Checks the robots.txt file for a given URL to see if scraping is allowed.
    Returns True if allowed or no robots.txt, False if disallowed.
    Note: This is a basic check and does not implement full robots.txt parsing.
    """
    parsed_url = urlparse(url)
    robots_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", '/robots.txt')
    try:
        response = requests.get(robots_url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            # A very basic check: if 'Disallow: /' is present, assume general disallow.
            # For a production system, use a proper robots.txt parser like 'robotparser'.
            if "Disallow: /" in response.text:
                print(f"Warning: robots.txt for {url} disallows scraping all paths.")
                return False
            return True
        else:
            # No robots.txt or other status code, generally assume it's okay to proceed
            return True
    except requests.exceptions.RequestException as e:
        print(f"Error checking robots.txt at {robots_url}: {e}. Proceeding assuming allowed.")
        return True # Default to True if robots.txt check fails

def scrape_content(url: str) -> str:
    """
    Scrapes content from a single URL using requests (for static content).
    This function focuses on extracting meaningful text content from the HTML.
    
    Args:
        url (str): The URL to scrape.
        
    Returns:
        str: The cleaned and processed text content from the URL, or an error message.
    """
    if not check_robots_txt(url):
        return f"Scraping of {url} is disallowed by robots.txt."

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements that are typically not part of the main content
        unwanted_tags = [
            'nav', 'header', 'footer', 'aside', 'script', 'style', 'noscript',
            'iframe', 'embed', 'object', 'applet', 'form', 'button', 'input',
            'select', 'textarea', 'fieldset', 'legend', 'optgroup', 'option',
            'img', 'svg', 'canvas', # Consider if images/visuals are needed. For text, remove.
            'audio', 'video'
        ]
        
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Remove elements with common ad/navigation/social classes or IDs
        unwanted_patterns = [
            'nav', 'navigation', 'menu', 'sidebar', 'ad', 'advertisement',
            'banner', 'header', 'footer', 'social', 'share', 'comment',
            'related', 'recommended', 'popular', 'trending', 'newsletter',
            'promo', 'popup', 'modal', 'overlay'
        ]
        
        for pattern in unwanted_patterns:
            # Find by class
            for element in soup.find_all(class_=lambda x: x and pattern in x.lower()):
                element.decompose()
            # Find by id
            for element in soup.find_all(id=lambda x: x and pattern in x.lower()):
                element.decompose()
        
        # Extract main content using common content containers
        main_content = None
        content_selectors = [
            'main', 'article', '.content', '.main-content', '.post-content',
            '.entry-content', '.article-content', '.page-content', '#content',
            '#main', '#primary', '.primary', '.main', 'body' # 'body' as a last resort
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if main_content:
            # Clean up whitespace and get text
            cleaned_content = main_content.get_text(separator='\n', strip=True)
            
            # Remove excessive whitespace and multiple spaces
            cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content) # Multiple newlines to double newline
            cleaned_content = re.sub(r' +', ' ', cleaned_content) # Multiple spaces to single space
            cleaned_content = re.sub(r'\t', ' ', cleaned_content) # Tabs to spaces
            
            return cleaned_content
        else:
            return "No main content found in the page."

    except requests.exceptions.RequestException as e:
        return f"Failed to retrieve {url}: {e}"
    except Exception as e:
        return f"An unexpected error occurred while processing {url}: {e}"

# Example of how you might use it if running directly, though the agent will call scrape_content
if __name__ == "__main__":
    # For local testing, read URLs from sites.txt
    try:
        with open('sites.txt', 'r', encoding='utf-8') as file:
            test_urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("sites.txt not found. Please create it with URLs for testing.")
        test_urls = ["https://www.cnbc.com/finance/", "https://finance.yahoo.com/news/"]

    print("--- Starting example scraping ---")
    for url in test_urls:
        processed_text = scrape_content(url)
        print(f"\n--- Processed content from {url} ---")
        print(processed_text[:500]) # Print first 500 characters for brevity
        print("...")

    # Clean up temp directory
    # import shutil
    # if os.path.exists(TEMP_UNPROCESSED_DIR):
    #     shutil.rmtree(TEMP_UNPROCESSED_DIR)