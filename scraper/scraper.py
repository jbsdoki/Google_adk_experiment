import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin

with open('sites.txt', 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file if line.strip()]

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

def scrape_urls(urls):
    for url in urls:
        check_robots_txt(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Generate a safe filename from the URL
        safe_filename = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
        output_filename = f'../storage/unprocessed/{safe_filename}.html'
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

def process_urls(files):
    for file in files:
        1


scrape_urls(urls)