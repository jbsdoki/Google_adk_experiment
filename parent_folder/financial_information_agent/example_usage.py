"""
Example usage of the financial information agents with shared tools.
This demonstrates how the agents can use the same functions but with different focuses.
"""

from stock_history_agent.agent import stock_history_investigator
from current_valuation_agent.agent import current_valuation_analyst
from future_outlook_agent.agent import future_outlook_analyst

def demonstrate_agent_capabilities():
    """Demonstrate how each agent can use the same tools differently."""
    
    # Example: Analyzing Apple (AAPL)
    symbol = "AAPL"
    
    print("=== Financial Information Agent Demo ===\n")
    
    # 1. Stock History Agent - focuses on historical analysis
    print("1. Stock History Investigator:")
    print(f"   - Available tools: {len(stock_history_investigator.tools)}")
    print(f"   - Focus: {stock_history_investigator.description}")
    print(f"   - Can access: get_comprehensive_company_info, analyze_financial_report, etc.")
    print()
    
    # 2. Current Valuation Agent - focuses on real-time metrics
    print("2. Current Valuation Analyst:")
    print(f"   - Available tools: {len(current_valuation_analyst.tools)}")
    print(f"   - Focus: {current_valuation_analyst.description}")
    print(f"   - Can access: get_stock_price, get_financial_metrics, etc.")
    print()
    
    # 3. Future Outlook Agent - focuses on news and sentiment
    print("3. Future Outlook Analyst:")
    print(f"   - Available tools: {len(future_outlook_analyst.tools)}")
    print(f"   - Focus: {future_outlook_analyst.description}")
    print(f"   - Can access: get_enhanced_company_news, scan_website_content, etc.")
    print()
    
    # Example of how agents might use the same function differently
    print("=== Example: Same Function, Different Use Cases ===")
    print()
    print("All agents can call get_comprehensive_company_info(symbol), but:")
    print("- Stock History Agent: Uses it to analyze long-term trends")
    print("- Current Valuation Agent: Uses it to get current financial ratios")
    print("- Future Outlook Agent: Uses it to understand company background for news analysis")
    print()

if __name__ == "__main__":
    demonstrate_agent_capabilities() 