"""
Shared tools module for all financial information agents.
This provides a centralized way for all agents to access the same web scraping and API functions.
"""

import sys
import os

# Add parent directory to path to import api_functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api_functions import (
    get_comprehensive_company_info,
    analyze_financial_report,
    get_company_wikipedia_info,
    get_realtime_stock_price,
    get_company_news,
    get_financial_metrics,
    get_stock_price,
    get_company_profile,
    get_enhanced_company_news,
    scan_website_content,
    check_robots_txt,
    scrape_raw_content,
    scrape_multiple_urls
)

# Define tool sets for different agent types
STOCK_HISTORY_TOOLS = [
    get_comprehensive_company_info,
    analyze_financial_report,
    get_company_wikipedia_info,
    get_realtime_stock_price,
    get_company_news,
    get_financial_metrics,
    check_robots_txt,
    scrape_raw_content
]

CURRENT_VALUATION_TOOLS = [
    get_stock_price,
    get_company_profile,
    get_financial_metrics,
    get_realtime_stock_price,
    get_comprehensive_company_info,
    check_robots_txt
]

FUTURE_OUTLOOK_TOOLS = [
    get_enhanced_company_news,
    scan_website_content,
    get_company_wikipedia_info,
    get_company_news,
    get_comprehensive_company_info,
    check_robots_txt,
    scrape_raw_content,
    scrape_multiple_urls
]

# All tools available to any agent
ALL_TOOLS = [
    get_comprehensive_company_info,
    analyze_financial_report,
    get_company_wikipedia_info,
    get_realtime_stock_price,
    get_company_news,
    get_financial_metrics,
    get_stock_price,
    get_company_profile,
    get_enhanced_company_news,
    scan_website_content,
    check_robots_txt,
    scrape_raw_content,
    scrape_multiple_urls
]

def get_tools_for_agent(agent_type: str) -> list:
    """
    Get the appropriate tools for a specific agent type.
    
    Args:
        agent_type (str): One of 'stock_history', 'current_valuation', 'future_outlook', or 'all'
    
    Returns:
        list: List of function references for the agent to use
    """
    tool_mapping = {
        'stock_history': STOCK_HISTORY_TOOLS,
        'current_valuation': CURRENT_VALUATION_TOOLS,
        'future_outlook': FUTURE_OUTLOOK_TOOLS,
        'all': ALL_TOOLS
    }
    
    return tool_mapping.get(agent_type, ALL_TOOLS) 