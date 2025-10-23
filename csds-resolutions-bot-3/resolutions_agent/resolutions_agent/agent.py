"""Agent to test out RAG engine to retrieve instructions from files."""

import os

from google.adk.agents import LlmAgent
from tools.tools import get_instructions_for_user_motivation

from utils import read_instructions_from_file

from .callbacks import add_instructions_callback, check_if_agent_should_run

description = """Agent to retrieve instructions to handle user requests.
Handles user intent classification and retrieves relevant step-by-step
instructions to solve users problem based on the user's classified intent."""

resolutions_agent = LlmAgent(
    name='retrieve_instructions_agent',
    model=os.environ.get('GOOGLE_CLOUD_LLM_NAME', ''),
    description=description,
    instruction=read_instructions_from_file(
        './resolutions_agent/instructions.md'
    ),
    tools=[get_instructions_for_user_motivation],
    before_agent_callback=check_if_agent_should_run,
    after_tool_callback=add_instructions_callback,
)
