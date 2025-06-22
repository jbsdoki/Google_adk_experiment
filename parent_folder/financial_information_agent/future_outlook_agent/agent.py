future_outlook_analyst = LlmAgent(
    name="future_outlook_analyst",
    model="gemini-2.5-pro",
    description=(
        "Analyzes web sentiment, real-time news, and public content to evaluate a company’s "
        "potential future performance and public perception."
    ),
    instruction=prompt.FUTURE_OUTLOOK_ANALYST_PROMPT,
    output_key="future_outlook_analyst_output",
    tools=[
        AgentTool(agent=get_enhanced_company_news),
        AgentTool(agent=scan_website_content),
        AgentTool(agent=get_company_wikipedia_info),
    ],
)
