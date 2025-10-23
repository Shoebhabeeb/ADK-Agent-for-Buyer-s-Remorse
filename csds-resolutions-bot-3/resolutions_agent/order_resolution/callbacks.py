"""Callbacks for the resolutions agent."""

from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from utils import read_instructions_from_file

# ruff: noqa: E501


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
    if current_state.get('instructions', False) and not current_state.get('instructions_filled', False):
        print(
            f'[Callback] State condition not met: Proceeding with agent {agent_name}.'
        )
        instructions = current_state.get('instructions')
        callback_context.agent_instruction_override = f"{read_instructions_from_file('./order_resolution/instructions.md')}\n\n### Historically Proven Steps ###\n{instructions}"
        print(f'[Callback] Agent instructions overridden with: {instructions[:30]}...')
        current_state['instructions_filled'] = True
        print(f'[Callback] State instructions filled: {current_state["instructions_filled"]}')
        # Return None to allow the LlmAgent's normal execution
        return None
    else:
        # Return Content to skip the agent's run
        return types.Content(
            parts=[
                types.Part(
                    text=f'Agent {agent_name} skipped by before_agent_callback due to state.'
                )
            ],
            role='model',  # Assign model role to the overriding response
        )