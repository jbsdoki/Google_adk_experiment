from . import prompt
import sys
import os

# Add parent directory to path to import shared_tools
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared_tools import get_tools_for_agent

class FutureOutlookAnalyst:
    def __init__(self):
        self.name = "future_outlook_analyst"
        self.description = (
            "Analyzes web sentiment, real-time news, and public content to evaluate a company's "
            "potential future performance and public perception."
        )
        self.instruction = prompt.FUTURE_OUTLOOK_ANALYST_PROMPT
        self.output_key = "future_outlook_analyst_output"
        self.tools = get_tools_for_agent('future_outlook')

future_outlook_analyst = FutureOutlookAnalyst()
