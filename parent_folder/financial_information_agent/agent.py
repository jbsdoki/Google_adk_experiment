from google.adk.agents import Agent
import sys
import os

# Add the parent directory to the Python path so we can import the scraper module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import scraper.scraper as scraper

# Add yfinance for real-time stock data
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance not installed. Install with: pip install yfinance")

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

def get_realtime_stock_price(symbol: str) -> dict:
    """
    Retrieves the real-time stock price for a given stock symbol using yfinance.
    
    Args:
        symbol (str): The stock ticker symbol (e.g., "GOOGL", "AAPL", "MSFT", "TSLA").
        
    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'price', 'currency', 
              'change', 'change_percent', 'volume', 'market_cap' or 'error_message'.
    """
    if not YFINANCE_AVAILABLE:
        return {
            "status": "error", 
            "error_message": "yfinance not available. Install with: pip install yfinance"
        }
    
    try:
        print(f"Fetching real-time stock price for: {symbol.upper()}")
        
        # Get stock info using yfinance
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        # Get current price and other data
        current_price = info.get('currentPrice', info.get('regularMarketPrice'))
        
        if not current_price:
            return {
                "status": "error", 
                "error_message": f"Could not retrieve price for {symbol.upper()}. Symbol may be invalid."
            }
        
        # Get additional information
        currency = info.get('currency', 'USD')
        previous_close = info.get('previousClose', current_price)
        change = current_price - previous_close if previous_close else 0
        change_percent = (change / previous_close * 100) if previous_close else 0
        volume = info.get('volume', 0)
        market_cap = info.get('marketCap', 0)
        company_name = info.get('longName', symbol.upper())
        
        return {
            "status": "success",
            "symbol": symbol.upper(),
            "company_name": company_name,
            "price": f"{current_price:.2f}",
            "currency": currency,
            "change": f"{change:+.2f}",
            "change_percent": f"{change_percent:+.2f}%",
            "volume": f"{volume:,}",
            "market_cap": f"${market_cap:,}" if market_cap else "N/A",
            "previous_close": f"{previous_close:.2f}"
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error fetching stock price for {symbol.upper()}: {str(e)}"
        }

def get_stock_price(symbol: str) -> dict:
    """
    Retrieves the current stock price for a given stock symbol.
    This function now uses the real-time stock price function.

    Args:
        symbol (str): The stock ticker symbol (e.g., "GOOGL", "AAPL", "MSFT").

    Returns:
        dict: A dictionary with stock price information or error message.
    """
    return get_realtime_stock_price(symbol)

def get_company_news(company_name: str) -> dict:
    """
    Fetches recent news articles related to a specific company using yfinance.
    This function can work with both company names and stock symbols.

    Args:
        company_name (str): The name of the company or stock symbol (e.g., "Google", "AAPL", "TSLA").

    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'news_articles' (list of news dictionaries)
              or 'error_message'.
    """
    if not YFINANCE_AVAILABLE:
        return {
            "status": "error", 
            "error_message": "yfinance not available. Install with: pip install yfinance"
        }
    
    try:
        print(f"Fetching real-time news for: {company_name}")
        
        # Try to get news using the company name/symbol
        ticker = yf.Ticker(company_name.upper())
        
        # Get news articles
        news = ticker.news
        
        if not news:
            return {
                "status": "error", 
                "error_message": f"No news found for {company_name}. Try using a stock symbol like 'AAPL' or 'TSLA'."
            }
        
        # Process news articles (limit to 10 most recent)
        processed_news = []
        for article in news[:10]:
            processed_news.append({
                "title": article.get('title', 'No title'),
                "summary": article.get('summary', 'No summary'),
                "publisher": article.get('publisher', 'Unknown'),
                "published": article.get('published', 'Unknown'),
                "url": article.get('link', ''),
                "sentiment": article.get('sentiment', 'neutral')
            })
        
        return {
            "status": "success",
            "company": company_name.upper(),
            "news_count": len(processed_news),
            "news_articles": processed_news
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error fetching news for {company_name}: {str(e)}"
        }

def analyze_financial_report(report_text: str) -> dict:
    """
    Analyzes a financial report or a block of financial text to identify key figures,
    trends, or sentiment. This is a conceptual tool that would use an LLM or NLP model.

    Args:
        report_text (str): The full text content of a financial report or relevant financial data.

    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'analysis' (summary/key points)
              or 'error_message'.
    """
    print(f"Agent is analyzing financial report (first 100 chars): {report_text[:100]}...")
    # In a real scenario, this would involve sending `report_text` to an LLM
    # or an NLP model for summarization, key phrase extraction, sentiment analysis, etc.
    if len(report_text) < 50:
        return {"status": "error", "error_message": "Report text is too short for meaningful analysis."}

    # Simple placeholder analysis
    keywords = ["revenue", "profit", "loss", "growth", "decline", "earnings", "outlook"]
    found_keywords = [kw for kw in keywords if kw in report_text.lower()]
    
    analysis_summary = "Preliminary analysis: "
    if "profit" in report_text.lower() and "growth" in report_text.lower():
        analysis_summary += "The report indicates positive growth and profitability. "
    elif "loss" in report_text.lower() or "decline" in report_text.lower():
        analysis_summary += "The report suggests areas of financial decline or loss. "
    else:
        analysis_summary += "General financial terms detected. "

    if found_keywords:
        analysis_summary += f"Key terms found: {', '.join(found_keywords)}."
    else:
        analysis_summary += "No specific financial keywords were immediately identified."

    return {"status": "success", "analysis": analysis_summary}


# Define your root agent
root_agent = Agent(
    name="financial_analyst_agent", # Changed agent name to reflect its new focus
    model="gemini-2.0-flash",
    description=(
        "An advanced financial analyst agent capable of scanning websites for content, "
        "retrieving real-time stock prices, fetching company news, and analyzing "
        "financial reports for key insights."
    ),
    instruction=(
        "You are a sophisticated financial analyst. "
        "When asked for stock prices, use the 'get_stock_price' tool. "
        "When asked for company news, use the 'get_company_news' tool. "
        "When a URL is provided for content extraction (e.g., articles, reports), "
        "use the 'scan_website_content' tool. "
        "If presented with text that appears to be a financial report or detailed financial data, "
        "use the 'analyze_financial_report' tool to provide a summary or insights. "
        "Always aim to provide concise and relevant financial information."
    ),
    tools=[scan_website_content, get_stock_price, get_company_news, analyze_financial_report],
)
