"""Callbacks for the resolutions agent."""

from typing import Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

# ruff: noqa: E501


def add_instructions_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict,
) -> None:
    """Callback to handle the response from the tool."""
    tool_context.state['instructions'] = tool_response
    if 'instructions_filled' not in tool_context.state:
        # Initialize instructions_filled to False if not already set
        # This ensures the state is ready for the agent's run
        tool_context.state['instructions_filled'] = False

def check_if_agent_should_run(
    callback_context: CallbackContext,
) -> types.Content | None:
    """Checks 'instructions' in session state."""
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f'\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})')
    print(f'[Callback] Current State: {current_state}')

    # Check the condition in session state dictionary
    if current_state.get('instructions', False):
        print(f'[Callback] Instructions filled : Skipping agent {agent_name}.')
        # Return Content to skip the agent's run
        return types.Content(
            parts=[
                types.Part(
                    text=f'Agent {agent_name} skipped by before_agent_callback due to state.'
                )
            ],
            role='model',  # Assign model role to the overriding response
        )
    else:
        print(
            f'[Callback] State condition not met: Proceeding with agent {agent_name}.'
        )
        # Return None to allow the LlmAgent's normal execution
        return None
