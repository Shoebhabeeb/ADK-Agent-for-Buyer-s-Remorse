"""Utility functions for the resolutions agent."""

from google.cloud import aiplatform_v1
from google.protobuf.json_format import MessageToDict


def read_instructions_from_file(filepath):
    """Reads the content of a file and returns it as a string."""
    with open(filepath, encoding='utf-8') as file:
        return file.read()


def extract_and_concatenate_rag_content(
    retrieval_response: aiplatform_v1.RetrieveContextsResponse,
    separator: str = '\n\n',
) -> str:
    """Extracts and concatenates the text.

    Args:
        retrieval_response (rag.RetrievalResponse): The response object
            obtained from a rag.retrieval_query call.
        separator (str): The string to use to join the retrieved text snippets.
                         Defaults to two newlines.

    Returns:
        str: A single string containing all extracted text snippets,
             concatenated with the specified separator. Returns an empty string
             if no content is retrieved or no snippets are found.
    """
    if not retrieval_response:
        return ''

    retrieval_response_dict = (
        MessageToDict(retrieval_response._pb)
        .get('contexts', {})
        .get('contexts', [])
    )

    retrieved_texts = []
    for i, context in enumerate(retrieval_response_dict):
        retrieved_texts.append(
            f"""Intent, Customer Motivation, Resolution Goals and
            Resolution Guide (step-by-step instructions) Example {i + 1}:
            {context.get('text', '')}\n\n"""
        )

    retrieved_texts = separator.join(retrieved_texts)

    return retrieved_texts
