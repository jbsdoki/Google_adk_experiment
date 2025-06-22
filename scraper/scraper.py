import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

with open('sites.txt', 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file if line.strip()]

def setup_driver():
    """Setup Chrome WebDriver with options for scraping"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")  # Don't load images to speed up
    chrome_options.add_argument("--disable-javascript")  # Disable JS for faster loading if not needed
    chrome_options.add_argument("--page-load-strategy=eager")  # Don't wait for all resources
    
    try:
        # Use webdriver-manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set timeouts
        driver.set_page_load_timeout(30)  # 30 seconds max for page load
        driver.implicitly_wait(10)  # 10 seconds max for finding elements
        
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Make sure Chrome browser is installed")
        return None

def check_robots_txt(url):
    parsed_url = urlparse(url)
    robots_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", '/robots.txt')
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            # print(f"robots.txt found at: {robots_url}")
            print(response.text)
            return True
        else:
            # print(f"No robots.txt found at: {robots_url}")
            return False
    except Exception as e:
        print(f"Error checking robots.txt at {robots_url}: {e}")
        return False

def needs_javascript(url):
    """Check if a URL likely needs JavaScript based on common patterns"""
    js_sites = [
        'react', 'vue', 'angular', 'spa', 'app', 'dashboard',
        'admin', 'portal', 'modern', 'dynamic', 'interactive'
    ]
    
    # Check if URL contains JavaScript-related keywords
    url_lower = url.lower()
    if any(keyword in url_lower for keyword in js_sites):
        return True
    
    # Check for common modern web frameworks
    modern_frameworks = [
        'nextjs', 'gatsby', 'nuxt', 'svelte', 'ember'
    ]
    
    if any(framework in url_lower for framework in modern_frameworks):
        return True
    
    return False

def scrape_urls(urls):
    driver = setup_driver()
    if not driver:
        print("Failed to setup WebDriver. Falling back to requests...")
        scrape_urls_requests(urls)
        return
    
    try:
        for url in urls:
            print(f"Scraping: {url}")
            check_robots_txt(url)
            
            # Decide whether to use Selenium or requests based on the URL
            use_selenium = needs_javascript(url)
            
            if use_selenium:
                print(f"Using Selenium for {url} (likely needs JavaScript)")
                success = scrape_with_selenium(driver, url)
                if not success:
                    print(f"Selenium failed, trying requests for {url}")
                    scrape_with_requests(url)
            else:
                print(f"Using requests for {url} (static content)")
                scrape_with_requests(url)
                
    finally:
        try:
            driver.quit()
        except:
            pass  # Ignore errors when quitting driver

def scrape_with_selenium(driver, url):
    """Scrape a single URL with Selenium"""
    try:
        # Navigate to the page with timeout
        driver.get(url)
        
        # Wait for page to load (shorter wait)
        time.sleep(2)
        
        # Try to wait for body, but don't hang if it fails
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            print(f"Warning: Could not find body element for {url}, continuing anyway...")
        
        # Get the page source after JavaScript has rendered
        page_source = driver.page_source
        
        # Generate a safe filename from the URL
        safe_filename = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
        output_filename = f'../storage/unprocessed/{safe_filename}.html'
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(page_source)
        
        print(f"Saved with Selenium: {output_filename}")
        return True
        
    except Exception as e:
        print(f"Error scraping {url} with Selenium: {e}")
        return False

def scrape_with_requests(url):
    """Scrape a single URL with requests"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        safe_filename = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
        output_filename = f'../storage/unprocessed/{safe_filename}.html'
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Saved with requests: {output_filename}")
        return True
        
    except Exception as e:
        print(f"Error scraping {url} with requests: {e}")
        return False

def scrape_urls_requests(urls):
    """Fallback method using requests for static content"""
    for url in urls:
        print(f"Scraping (requests): {url}")
        check_robots_txt(url)
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Generate a safe filename from the URL
            safe_filename = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
            output_filename = f'../storage/unprocessed/{safe_filename}.html'
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Saved: {output_filename}")
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            continue

def process_urls(files):
    # Create processed directory if it doesn't exist
    processed_dir = '../storage/processed'
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    
    for file in files:
        file_path = f'../storage/unprocessed/{file}'
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove unwanted elements
        unwanted_tags = [
            'nav', 'header', 'footer', 'aside', 'script', 'style', 'noscript',
            'iframe', 'embed', 'object', 'applet', 'form', 'button', 'input',
            'select', 'textarea', 'fieldset', 'legend', 'optgroup', 'option'
        ]
        
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Remove elements with common ad/navigation classes
        unwanted_classes = [
            'nav', 'navigation', 'menu', 'sidebar', 'ad', 'advertisement',
            'banner', 'header', 'footer', 'social', 'share', 'comment',
            'related', 'recommended', 'popular', 'trending', 'newsletter'
        ]
        
        for class_name in unwanted_classes:
            for element in soup.find_all(class_=lambda x: x and class_name in x.lower()):
                element.decompose()
        
        # Remove elements with common ad/navigation IDs
        unwanted_ids = [
            'nav', 'navigation', 'menu', 'sidebar', 'ad', 'advertisement',
            'banner', 'header', 'footer', 'social', 'share', 'comment'
        ]
        
        for id_name in unwanted_ids:
            for element in soup.find_all(id=lambda x: x and id_name in x.lower()):
                element.decompose()
        
        # Extract main content (focus on common content containers)
        main_content = None
        content_selectors = [
            'main', 'article', '.content', '.main-content', '.post-content',
            '.entry-content', '.article-content', '.page-content', '#content',
            '#main', '#primary', '.primary', '.main'
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            # Fallback: use body but remove more noise
            main_content = soup.find('body')
            if main_content:
                # Remove more noise from body
                for element in main_content.find_all(['div', 'section']):
                    if element.get('class') and any(cls in str(element.get('class')).lower() for cls in ['nav', 'menu', 'sidebar', 'ad', 'banner']):
                        element.decompose()
        
        if main_content:
            # Clean up whitespace and get text
            cleaned_content = main_content.get_text(separator='\n', strip=True)
            
            # Remove excessive whitespace
            cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content)
            cleaned_content = re.sub(r' +', ' ', cleaned_content)
            
            # Save to processed directory
            output_file = f'{processed_dir}/{file.replace(".html", "_processed.txt")}'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"Processed: {file} -> {file.replace('.html', '_processed.txt')}")
        else:
            print(f"No main content found in: {file}")

scrape_urls(urls)

# Process the scraped files
unprocessed_files = [f for f in os.listdir('../storage/unprocessed') if f.endswith('.html')]
process_urls(unprocessed_files)