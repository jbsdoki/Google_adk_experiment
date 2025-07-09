import requests
from urllib.parse import urlparse, urljoin


def check_robots_txt(url: str) -> dict:
    """
    Checks the robots.txt file for a given URL to see if scraping is allowed.
    
    Args:
        url (str): The URL to check robots.txt for
        
    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'allowed' (boolean)
              or 'error_message' if something went wrong.
    """
    try:
        parsed_url = urlparse(url)
        robots_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", '/robots.txt')
        
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            # Basic check: if 'Disallow: /' is present, assume general disallow
            if "Disallow: /" in response.text:
                return {
                    "status": "success",
                    "allowed": False,
                    "message": f"Scraping of {url} is disallowed by robots.txt"
                }
            return {
                "status": "success",
                "allowed": True,
                "message": f"Scraping of {url} appears to be allowed by robots.txt"
            }
        else:
            # No robots.txt or other status code, generally assume it's okay
            return {
                "status": "success",
                "allowed": True,
                "message": f"No robots.txt found for {url}, assuming scraping is allowed"
            }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Error checking robots.txt at {url}: {str(e)}"
        }

def scrape_raw_content(url: str) -> dict:
    """
    Scrapes raw HTML content from a URL without cleaning or processing.
    Useful for when you need the full HTML structure.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'html_content' 
              or 'error_message' if something went wrong.
    """
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        return {
            "status": "success",
            "html_content": response.text,
            "url": url,
            "status_code": response.status_code
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve {url}: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred while processing {url}: {str(e)}"
        }

def scrape_multiple_urls(urls: list) -> dict:
    """
    Scrapes content from multiple URLs and returns results for each.
    
    Args:
        urls (list): List of URLs to scrape
        
    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'results' 
              (list of scraping results) or 'error_message'.
    """
    if not urls:
        return {
            "status": "error",
            "error_message": "No URLs provided"
        }
    
    results = []
    for url in urls:
        result = scan_website_content(url)
        results.append({
            "url": url,
            "result": result
        })
    
    return {
        "status": "success",
        "total_urls": len(urls),
        "results": results
    }

# New tool for scanning website content (from previous version)
def scan_website_content(url: str) -> dict:
    """
    Scans a given URL and extracts the main text content, cleaning out noise.
    This tool is suitable for extracting articles, reports, or general text
    from web pages, especially financial news or information sites.

    Args:
        url (str): The URL of the website to scan.

    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'content' (the scraped text)
              or 'error_message' if something went wrong.
    """
    print(f"Agent is calling scrape_content for URL: {url}")
    scraped_text = scraper.scrape_content(url)
    if "Failed to retrieve" in scraped_text or "No main content found" in scraped_text or "disallowed by robots.txt" in scraped_text:
        return {"status": "error", "error_message": scraped_text}
    else:
        return {"status": "success", "content": scraped_text}
