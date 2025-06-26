from . import prompt
import sys
import os

# Add parent directory to path to import shared_tools
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared_tools import get_tools_for_agent

# For now, let's create a simple agent class until you decide on your agent framework
class StockHistoryInvestigator:
    def __init__(self):
        self.name = "stock_history_investigator"
        self.description = (
            "Analyzes a stock's historical performance including long-term trends, "
            "earnings reports, and major corporate events."
        )
        self.instruction = prompt.STOCK_HISTORY_INVESTIGATOR_PROMPT
        self.output_key = "stock_history_investigator_output"
        self.tools = get_tools_for_agent('stock_history')

stock_history_investigator = StockHistoryInvestigator()
