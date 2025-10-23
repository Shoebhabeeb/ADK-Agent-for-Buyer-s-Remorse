"""Utility functions for working with Vertex AI RAG."""

import vertexai
from vertexai import rag


def create_rag_corpus(
    project_id: str,
    display_name: str,
    embedding_model: str = 'publishers/google/models/text-embedding-005',
    location: str = 'us-central1',
):
    """Create a RAG Corpus, Import Files, and Generate a response.

    Args:
        project_id (str): The ID of your Google Cloud project.
        display_name (str): The display name for the RAG corpus.
        embedding_model (str): The embedding model to use for the RAG corpus.
        location (str): The location for the RAG corpus
    """
    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location=location)

    # Create RagCorpus
    # Configure embedding model, for example "text-embedding-005".
    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model=embedding_model
        )
    )

    rag_corpus = rag.create_corpus(
        display_name=display_name,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        ),
    )

    return rag_corpus


def import_files_to_rag_corpus(rag_corpus: rag.RagCorpus, paths: list[str]):
    """Import files to the RAG corpus.

    Args:
       rag_corpus (rag.RagCorpus): The RAG corpus to import files into.
       paths (list[str]): List of GCS paths to the files to be imported.
    """
    # Import Files to the RagCorpus
    rag.import_files(
        rag_corpus.name,  # type: ignore
        paths,
    )


def _retrieve_response(rag_corpus: rag.RagCorpus):
    """Generate a response using the RAG corpus.

    Args:
        rag_corpus (rag.RagCorpus): The RAG corpus to use for retrieval.
    """
    # Direct context retrieval
    rag_retrieval_config = rag.RagRetrievalConfig(
        top_k=3,  # Optional
        filter=rag.Filter(vector_distance_threshold=0.5),  # Optional
    )

    response = rag.retrieval_query(
        rag_resources=[
            rag.RagResource(
                rag_corpus=rag_corpus.name,
                # Optional: supply IDs from `rag.list_files()`.
                # rag_file_ids=["rag-file-1", "rag-file-2", ...],
            )
        ],
        text='What is RAG and why it is helpful?',
        rag_retrieval_config=rag_retrieval_config,
    )
    print(response)

    return response
