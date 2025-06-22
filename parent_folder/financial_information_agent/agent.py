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

def get_company_profile(symbol: str) -> dict:
    """
    Gets comprehensive company profile information using yfinance.
    
    Args:
        symbol (str): The stock ticker symbol (e.g., "TSLA", "AAPL", "GOOGL").
        
    Returns:
        dict: A dictionary with comprehensive company information.
    """
    if not YFINANCE_AVAILABLE:
        return {
            "status": "error", 
            "error_message": "yfinance not available. Install with: pip install yfinance"
        }
    
    try:
        print(f"Fetching company profile for: {symbol.upper()}")
        
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        # Extract key company information
        profile = {
            "status": "success",
            "symbol": symbol.upper(),
            "company_name": info.get('longName', symbol.upper()),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "description": info.get('longBusinessSummary', 'No description available'),
            "website": info.get('website', 'N/A'),
            "employees": info.get('fullTimeEmployees', 'N/A'),
            "country": info.get('country', 'N/A'),
            "city": info.get('city', 'N/A'),
            "state": info.get('state', 'N/A'),
            "founded": info.get('founded', 'N/A'),
            "ceo": info.get('companyOfficers', [{}])[0].get('name', 'N/A') if info.get('companyOfficers') else 'N/A',
            "market_cap": f"${info.get('marketCap', 0):,}" if info.get('marketCap') else 'N/A',
            "enterprise_value": f"${info.get('enterpriseValue', 0):,}" if info.get('enterpriseValue') else 'N/A',
            "pe_ratio": f"{info.get('trailingPE', 0):.2f}" if info.get('trailingPE') else 'N/A',
            "forward_pe": f"{info.get('forwardPE', 0):.2f}" if info.get('forwardPE') else 'N/A',
            "price_to_book": f"{info.get('priceToBook', 0):.2f}" if info.get('priceToBook') else 'N/A',
            "debt_to_equity": f"{info.get('debtToEquity', 0):.2f}" if info.get('debtToEquity') else 'N/A',
            "profit_margins": f"{info.get('profitMargins', 0)*100:.2f}%" if info.get('profitMargins') else 'N/A',
            "revenue_growth": f"{info.get('revenueGrowth', 0)*100:.2f}%" if info.get('revenueGrowth') else 'N/A',
            "52_week_high": f"${info.get('fiftyTwoWeekHigh', 0):.2f}" if info.get('fiftyTwoWeekHigh') else 'N/A',
            "52_week_low": f"${info.get('fiftyTwoWeekLow', 0):.2f}" if info.get('fiftyTwoWeekLow') else 'N/A',
            "beta": f"{info.get('beta', 0):.2f}" if info.get('beta') else 'N/A',
            "dividend_yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else 'N/A'
        }
        
        return profile
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error fetching company profile for {symbol.upper()}: {str(e)}"
        }

def get_financial_metrics(symbol: str) -> dict:
    """
    Gets detailed financial metrics and ratios for a company.
    
    Args:
        symbol (str): The stock ticker symbol.
        
    Returns:
        dict: A dictionary with financial metrics and ratios.
    """
    if not YFINANCE_AVAILABLE:
        return {
            "status": "error", 
            "error_message": "yfinance not available. Install with: pip install yfinance"
        }
    
    try:
        print(f"Fetching financial metrics for: {symbol.upper()}")
        
        ticker = yf.Ticker(symbol.upper())
        
        # Get financial statements
        income_stmt = ticker.income_stmt
        balance_sheet = ticker.balance_sheet
        cash_flow = ticker.cashflow
        
        # Get latest annual data
        if not income_stmt.empty:
            latest_revenue = income_stmt.loc['Total Revenue'].iloc[0] if 'Total Revenue' in income_stmt.index else 0
            latest_net_income = income_stmt.loc['Net Income'].iloc[0] if 'Net Income' in income_stmt.index else 0
        else:
            latest_revenue = 0
            latest_net_income = 0
            
        if not balance_sheet.empty:
            latest_assets = balance_sheet.loc['Total Assets'].iloc[0] if 'Total Assets' in balance_sheet.index else 0
            latest_liabilities = balance_sheet.loc['Total Liabilities'].iloc[0] if 'Total Liabilities' in balance_sheet.index else 0
        else:
            latest_assets = 0
            latest_liabilities = 0
        
        metrics = {
            "status": "success",
            "symbol": symbol.upper(),
            "revenue": f"${latest_revenue:,.0f}" if latest_revenue else 'N/A',
            "net_income": f"${latest_net_income:,.0f}" if latest_net_income else 'N/A',
            "total_assets": f"${latest_assets:,.0f}" if latest_assets else 'N/A',
            "total_liabilities": f"${latest_liabilities:,.0f}" if latest_liabilities else 'N/A',
            "return_on_equity": f"{(latest_net_income / (latest_assets - latest_liabilities) * 100):.2f}%" if (latest_assets - latest_liabilities) > 0 else 'N/A',
            "return_on_assets": f"{(latest_net_income / latest_assets * 100):.2f}%" if latest_assets > 0 else 'N/A'
        }
        
        return metrics
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error fetching financial metrics for {symbol.upper()}: {str(e)}"
        }

def get_enhanced_company_news(symbol: str) -> dict:
    """
    Gets enhanced news with better error handling and content extraction.
    
    Args:
        symbol (str): The stock ticker symbol.
        
    Returns:
        dict: A dictionary with enhanced news information.
    """
    if not YFINANCE_AVAILABLE:
        return {
            "status": "error", 
            "error_message": "yfinance not available. Install with: pip install yfinance"
        }
    
    try:
        print(f"Fetching enhanced news for: {symbol.upper()}")
        
        ticker = yf.Ticker(symbol.upper())
        news = ticker.news
        
        if not news:
            return {
                "status": "error", 
                "error_message": f"No news found for {symbol.upper()}"
            }
        
        # Process news with better error handling
        processed_news = []
        for article in news[:10]:
            try:
                processed_article = {
                    "title": article.get('title', 'No title available'),
                    "summary": article.get('summary', 'No summary available'),
                    "publisher": article.get('publisher', 'Unknown publisher'),
                    "published": article.get('published', 'Unknown date'),
                    "url": article.get('link', ''),
                    "sentiment": article.get('sentiment', 'neutral')
                }
                processed_news.append(processed_article)
            except Exception as e:
                print(f"Error processing article: {e}")
                continue
        
        return {
            "status": "success",
            "symbol": symbol.upper(),
            "news_count": len(processed_news),
            "news_articles": processed_news
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error fetching news for {symbol.upper()}: {str(e)}"
        }

def get_company_wikipedia_info(company_name: str) -> dict:
    """
    Scrapes additional company information from Wikipedia and other sources.
    This complements the API data with more detailed background information.
    
    Args:
        company_name (str): The company name or symbol to search for.
        
    Returns:
        dict: A dictionary with additional company information from web sources.
    """
    try:
        print(f"Fetching Wikipedia info for: {company_name}")
        
        # Try to get Wikipedia info using the scraper
        # First try with company name
        wiki_url = f"https://en.wikipedia.org/wiki/{company_name.replace(' ', '_')}"
        
        # Use the scraper to get content
        scraped_content = scraper.scrape_content(wiki_url)
        
        if "Failed to retrieve" in scraped_content or "No main content found" in scraped_content:
            # Try alternative search
            search_url = f"https://en.wikipedia.org/wiki/Special:Search/{company_name.replace(' ', '_')}"
            scraped_content = scraper.scrape_content(search_url)
        
        if "Failed to retrieve" in scraped_content or "No main content found" in scraped_content:
            return {
                "status": "error",
                "error_message": f"Could not find Wikipedia information for {company_name}"
            }
        
        # Extract key information from the scraped content
        content_lower = scraped_content.lower()
        
        # Look for key information patterns
        info = {
            "status": "success",
            "company_name": company_name,
            "source": "Wikipedia",
            "content_preview": scraped_content[:500] + "..." if len(scraped_content) > 500 else scraped_content,
            "key_facts": {}
        }
        
        # Extract founding year if present
        import re
        founding_match = re.search(r'founded[^0-9]*(\d{4})', content_lower)
        if founding_match:
            info["key_facts"]["founded"] = founding_match.group(1)
        
        # Extract headquarters if present
        hq_match = re.search(r'headquarters[^.]*\.', content_lower)
        if hq_match:
            info["key_facts"]["headquarters"] = hq_match.group(0).replace('headquarters', '').strip(' .')
        
        # Extract CEO if present
        ceo_match = re.search(r'ceo[^.]*\.', content_lower)
        if ceo_match:
            info["key_facts"]["ceo"] = ceo_match.group(0).replace('ceo', '').strip(' .')
        
        return info
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching Wikipedia info for {company_name}: {str(e)}"
        }

def get_comprehensive_company_info(symbol: str) -> dict:
    """
    Gets comprehensive company information by combining multiple sources.
    This is the main function that aggregates all company data.
    
    Args:
        symbol (str): The stock ticker symbol.
        
    Returns:
        dict: A comprehensive dictionary with all available company information.
    """
    print(f"Getting comprehensive information for: {symbol.upper()}")
    
    # Get all available information
    stock_price = get_realtime_stock_price(symbol)
    company_profile = get_company_profile(symbol)
    financial_metrics = get_financial_metrics(symbol)
    enhanced_news = get_enhanced_company_news(symbol)
    
    # Try to get Wikipedia info using company name
    company_name = company_profile.get('company_name', symbol) if company_profile.get('status') == 'success' else symbol
    wiki_info = get_company_wikipedia_info(company_name)
    
    # Compile comprehensive report
    comprehensive_info = {
        "status": "success",
        "symbol": symbol.upper(),
        "timestamp": "Current",
        "stock_price": stock_price,
        "company_profile": company_profile,
        "financial_metrics": financial_metrics,
        "news": enhanced_news,
        "additional_info": wiki_info
    }
    
    return comprehensive_info

# Define your root agent
root_agent = Agent(
    name="financial_analyst_agent", # Changed agent name to reflect its new focus
    model="gemini-2.0-flash",
    description=(
        "An advanced financial analyst agent capable of providing comprehensive company information, "
        "real-time stock prices, financial metrics, company profiles, news analysis, and web content scraping. "
        "This agent combines multiple data sources including APIs and web scraping for complete financial analysis."
    ),
    instruction=(
        "You are a sophisticated financial analyst with access to comprehensive company data. "
        "When asked for stock prices, use the 'get_stock_price' tool for real-time data. "
        "When asked for company news, use the 'get_enhanced_company_news' tool for detailed news with summaries. "
        "When asked for comprehensive company information, use the 'get_comprehensive_company_info' tool. "
        "For specific company profiles, use 'get_company_profile'. "
        "For financial metrics and ratios, use 'get_financial_metrics'. "
        "When a URL is provided for content extraction, use the 'scan_website_content' tool. "
        "If presented with text that appears to be a financial report, use the 'analyze_financial_report' tool. "
        "Always provide detailed, well-structured responses with relevant financial context and insights."
    ),
    tools=[
        scan_website_content, 
        get_stock_price, 
        get_enhanced_company_news, 
        analyze_financial_report, 
        get_company_profile, 
        get_financial_metrics, 
        get_comprehensive_company_info,
        get_company_wikipedia_info
    ],
)
