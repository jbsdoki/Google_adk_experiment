from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from . import prompt

stock_history_investigator = LlmAgent(
    name="stock_history_investigator",
    model="gemini-2.5-pro",
    description=(
        "Analyzes a stock’s historical performance including long-term trends, "
        "earnings reports, and major corporate events."
    ),
    instruction=prompt.STOCK_HISTORY_INVESTIGATOR_PROMPT,
    output_key="stock_history_investigator_output",
    tools=[
        AgentTool(agent=get_comprehensive_company_info),
        AgentTool(agent=analyze_financial_report),
        AgentTool(agent=get_company_wikipedia_info),
    ],
)
