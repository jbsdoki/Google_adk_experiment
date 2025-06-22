import yfinance as yf
import pandas as pd # yfinance often returns data in pandas DataFrames

def get_realtime_stock_price(symbol: str) -> dict:
    """
    Retrieves the current stock price for a given stock ticker symbol using yfinance.

    Args:
        symbol (str): The stock ticker symbol (e.g., "GOOG", "AAPL", "MSFT").

    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'price' or 'error_message'.
    """
    try:
        ticker = yf.Ticker(symbol)
        # Get the most recent info, which includes current price for active markets
        # Note: 'info' field might not be real-time for all stocks/markets
        # A more robust way for "current price" might be to get latest daily close
        # or use streaming data if truly real-time is needed.
        # For simple current price, 'regularMarketPrice' or 'currentPrice' from info
        # is often sufficient during market hours.
        info = ticker.info

        # Prioritize 'currentPrice' if available, otherwise fall back to 'regularMarketPrice'
        price = info.get('currentPrice')
        if price is None:
            price = info.get('regularMarketPrice')

        if price is not None:
            currency = info.get('currency', 'USD') # Get currency if available
            return {"status": "success", "price": f"{price:.2f} {currency}"}
        else:
            return {"status": "error", "error_message": f"Could not retrieve live price for {symbol}. Data might be delayed or unavailable."}
    except Exception as e:
        return {"status": "error", "error_message": f"Error fetching stock price for {symbol}: {e}"}

def get_realtime_company_news(symbol: str) -> dict:
    """
    Fetches recent news articles related to a specific company using yfinance.

    Args:
        symbol (str): The stock ticker symbol (e.g., "GOOG", "AAPL", "MSFT").

    Returns:
        dict: A dictionary with 'status' ("success" or "error") and 'news_articles' (list of news dictionaries)
              or 'error_message'. Each news dictionary includes 'title', 'publisher', and 'link'.
    """
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news

        if news:
            # Extract relevant information from each news item
            news_list = []
            for item in news:
                news_list.append({
                    "title": item.get('title', 'N/A'),
                    "publisher": item.get('publisher', 'N/A'),
                    "link": item.get('link', 'N/A')
                })
            return {"status": "success", "news_articles": news_list}
        else:
            return {"status": "error", "error_message": f"No recent news found for {symbol}."}
    except Exception as e:
        return {"status": "error", "error_message": f"Error fetching company news for {symbol}: {e}"}

# Example usage (for testing this file directly)
if __name__ == "__main__":
    print("--- Testing get_realtime_stock_price ---")
    stock_price_goog = get_realtime_stock_price("GOOG")
    print(f"GOOG price: {stock_price_goog}")

    stock_price_msft = get_realtime_stock_price("MSFT")
    print(f"MSFT price: {stock_price_msft}")

    stock_price_invalid = get_realtime_stock_price("INVALID")
    print(f"INVALID price: {stock_price_invalid}")

    print("\n--- Testing get_realtime_company_news ---")
    company_news_aapl = get_realtime_company_news("AAPL")
    if company_news_aapl['status'] == 'success':
        print(f"Recent news for AAPL ({len(company_news_aapl['news_articles'])} articles):")
        for i, article in enumerate(company_news_aapl['news_articles'][:3]): # Print first 3 for brevity
            print(f"  {i+1}. Title: {article['title']}\n     Publisher: {article['publisher']}\n     Link: {article['link']}")
        if len(company_news_aapl['news_articles']) > 3:
            print("  ...")
    else:
        print(f"AAPL news: {company_news_aapl['error_message']}")

    company_news_tsla = get_realtime_company_news("TSLA")
    if company_news_tsla['status'] == 'success':
        print(f"\nRecent news for TSLA ({len(company_news_tsla['news_articles'])} articles):")
        for i, article in enumerate(company_news_tsla['news_articles'][:3]): # Print first 3
            print(f"  {i+1}. Title: {article['title']}\n     Publisher: {article['publisher']}\n     Link: {article['link']}")
        if len(company_news_tsla['news_articles']) > 3:
            print("  ...")
    else:
        print(f"TSLA news: {company_news_tsla['error_message']}")
