 current_valuation_analyst = LlmAgent(
    name="current_valuation_analyst",
    model="gemini-2.5-pro",
    description=(
        "Delivers a real-time snapshot of a company’s financial health, valuation ratios, "
        "and core profile information."
    ),
    instruction=prompt.CURRENT_VALUATION_ANALYST_PROMPT,
    output_key="current_valuation_analyst_output",
    tools=[
        AgentTool(agent=get_stock_price),
        AgentTool(agent=get_company_profile),
        AgentTool(agent=get_financial_metrics),
    ],
)
