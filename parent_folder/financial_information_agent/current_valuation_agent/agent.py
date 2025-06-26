from . import prompt
import sys
import os

# Add parent directory to path to import shared_tools
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared_tools import get_tools_for_agent

class CurrentValuationAnalyst:
    def __init__(self):
        self.name = "current_valuation_analyst"
        self.description = (
            "Delivers a real-time snapshot of a company's financial health, valuation ratios, "
            "and core profile information."
        )
        self.instruction = prompt.CURRENT_VALUATION_ANALYST_PROMPT
        self.output_key = "current_valuation_analyst_output"
        self.tools = get_tools_for_agent('current_valuation')

current_valuation_analyst = CurrentValuationAnalyst()
