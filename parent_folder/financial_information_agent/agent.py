from google.adk.agents import Agent
import scraper # Import your updated scraper.py

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


def get_stock_price(symbol: str) -> dict:
    """
    Retrieves the current stock price for a given stock symbol.
    This is a placeholder and would connect to a real-time stock API in a full implementation.

    Args:
        symbol (str): The stock ticker symbol (e.g., "GOOG", "AAPL", "MSFT").

    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'price' or 'error_message'.
    """
    print(f"Agent is attempting to get stock price for: {symbol}")
    # Placeholder for actual API call
    if symbol.upper() == "GOOG":
        return {"status": "success", "price": "180.50 USD"}
    elif symbol.upper() == "AAPL":
        return {"status": "success", "price": "215.75 USD"}
    elif symbol.upper() == "MSFT":
        return {"status": "success", "price": "450.10 USD"}
    else:
        return {"status": "error", "error_message": f"Stock price for '{symbol}' not found or not supported."}

def get_company_news(company_name: str) -> dict:
    """
    Fetches recent news articles related to a specific company.
    This is a placeholder and would connect to a news API in a full implementation.

    Args:
        company_name (str): The name of the company (e.g., "Google", "Apple").

    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'news_articles' (list of news snippets)
              or 'error_message'.
    """
    print(f"Agent is fetching news for: {company_name}")
    # Placeholder for actual API call or targeted scraping
    if "google" in company_name.lower():
        return {
            "status": "success",
            "news_articles": [
                "Google announces new AI initiatives.",
                "Alphabet Q2 earnings report exceeds expectations.",
                "Google Cloud expands partnership with major bank."
            ]
        }
    elif "apple" in company_name.lower():
        return {
            "status": "success",
            "news_articles": [
                "Apple unveils new iPhone model.",
                "Apple Services revenue continues to grow.",
                "Supply chain issues may impact Apple production."
            ]
        }
    else:
        return {"status": "error", "error_message": f"News for '{company_name}' not found."}

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

def get_company_news(company_name: str) -> dict:
    """
    Fetches recent news articles related to a specific company using the yfinance API.
    Note: yfinance news lookup is based on ticker symbol, so the agent might need to infer
    the symbol from the company name or the user needs to provide the symbol.

    Args:
        company_name (str): The name of the company (e.g., "Google", "Apple").
                            For best results, provide a stock symbol if possible.

    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'news_articles' (list of news dictionaries)
              or 'error_message'.
    """
    print(f"Agent is fetching real-time news for: {company_name}")
    # In a more advanced agent, you might add a mapping from company name to symbol
    # For now, let's assume the agent can infer common symbols or the user provides it.
    # Otherwise, you might need an additional step (e.g., another tool or internal logic)
    # to convert company name to symbol.
    # --- CHANGE THIS LINE ---
    return financial_api_tools.get_realtime_company_news(company_name) # Assuming company_name can be a symbol


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
