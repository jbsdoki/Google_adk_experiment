from .api_functions import *
from .stock_history_agent.agent import stock_history_investigator
from .current_valuation_agent.agent import current_valuation_analyst
from .future_outlook_agent.agent import future_outlook_analyst

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

root_stock_agent = LlmAgent(
    name="stock_master_analyst",
    model="gemini-2.5-pro",
    description=(
        "Directs user queries to specialized stock agents for historical analysis, "
        "current valuation, or predictive forecasting based on user goals."
    ),
    instruction="""
Role: I am your stock analysis coordinator.
Ask me any question about a company's history, current value, or future potential, and I will route it to the best agent.
""",
    output_key="stock_master_analyst_output",
    tools=[
        AgentTool(agent=stock_history_investigator),
        AgentTool(agent=current_valuation_analyst),
        AgentTool(agent=future_outlook_analyst),
    ],
)
