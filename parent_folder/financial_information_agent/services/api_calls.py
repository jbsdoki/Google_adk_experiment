import yfinance as yf
import requests
from typing import Dict, Any

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
