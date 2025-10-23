"""Sequential agent for the resoltuons agent."""

from google.adk.agents import SequentialAgent
from order_resolution.agent import order_resolver

from resolutions_agent.agent import resolutions_agent

code_pipeline_agent = SequentialAgent(
    name='ResolutionsPipelineAgent',
    sub_agents=[resolutions_agent, order_resolver],
    description="""Identifies user intent and resolves issues by retrieving
        instructions and handling order-related requests.""",
)

# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = code_pipeline_agent
