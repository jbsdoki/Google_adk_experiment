# CAL AI 2025 - Financial Information Agent

A comprehensive financial information system built using Google's Agent Development Kit (ADK) that provides current valuation, future outlook, and stock history analysis.

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- Google ADK API access

## Getting a Google ADK API Key

### Step 1: Set up Google Cloud Platform
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable billing for your project (required for API usage)

### Step 2: Enable the ADK API
1. In the Google Cloud Console, navigate to "APIs & Services" > "Library"
2. Search for "Agent Development Kit" or "ADK"
3. Click on the ADK API and press "Enable"

### Step 3: Create API Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API Key"
3. Copy the generated API key
4. (Optional) Restrict the API key to specific APIs and IP addresses for security

### Step 4: Set up Environment Variables
1. Navigate to the `parent_folder/financial_information_agent/` directory
2. Create a `.env` file if it doesn't exist
3. Add your API key to the `.env` file:
   ```
   GOOGLE_ADK_API_KEY=your_api_key_here
   ```

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd CAL_AI_2025
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables as described above

## Project Structure

```
CAL_AI_2025/
├── parent_folder/
│   └── financial_information_agent/
│       ├── agent.py                 # Main agent implementation
│       ├── api_functions.py         # API integration functions
│       ├── current_valuation_agent/ # Current valuation analysis
│       ├── future_outlook_agent/    # Future outlook predictions
│       ├── stock_history_agent/     # Historical data analysis
│       ├── shared_tools.py          # Shared utilities
│       └── .env                     # Environment variables (create this)
├── scraper/                         # Web scraping utilities
├── storage/                         # Data storage
└── documentation.md                 # Project documentation
```

## Usage

1. Ensure your `.env` file is properly configured with your Google ADK API key
2. Run the main agent:
   ```bash
   python parent_folder/financial_information_agent/agent.py
   ```

3. For specific functionality, you can run individual agents:
   ```bash
   # Current valuation analysis
   python parent_folder/financial_information_agent/current_valuation_agent/agent.py
   
   # Future outlook analysis
   python parent_folder/financial_information_agent/future_outlook_agent/agent.py
   
   # Stock history analysis
   python parent_folder/financial_information_agent/stock_history_agent/agent.py
   ```

## Features

- **Current Valuation Agent**: Analyzes current stock valuations and market conditions
- **Future Outlook Agent**: Provides predictions and future market analysis
- **Stock History Agent**: Processes historical stock data and trends
- **Web Scraping**: Automated data collection from financial websites

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and restrict them appropriately
- Monitor your API usage to avoid unexpected charges

## Troubleshooting

### API Key Issues
- Ensure your API key is correctly formatted in the `.env` file
- Verify that the ADK API is enabled in your Google Cloud Console
- Check that billing is enabled for your Google Cloud project

### Common Errors
- `ModuleNotFoundError`: Install missing dependencies with `pip install -r requirements.txt`
- `API Key not found`: Verify your `.env` file exists and contains the correct API key
- `Permission denied`: Check that your API key has the necessary permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues related to Google ADK, refer to the [official documentation](https://google.github.io/adk-docs/).