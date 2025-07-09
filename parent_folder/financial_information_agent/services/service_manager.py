from .api_calls import (
    get_realtime_stock_price,
    get_stock_price,
    get_company_news,
    analyze_financial_report,
    get_company_profile,
    get_financial_metrics,
    get_enhanced_company_news,
)
from .web_scraper import (
    check_robots_txt,
    scrape_raw_content,
    scrape_multiple_urls,
    scan_website_content,
)

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
    wiki_info = None
    
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

