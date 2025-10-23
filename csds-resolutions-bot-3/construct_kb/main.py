"""Create a RAG Corpus, Import Files, and Generate a response."""

from utils.upload_to_gcs import upload_json_file_to_gcs
from utils.vertexai_rag_utils import (
    _retrieve_response,
    create_rag_corpus,
    import_files_to_rag_corpus,
)

if __name__ == '__main__':
    # upload a JSON file to GCS
    project_id = 'hd-contactctr-dev'
    bucket_name = 'csds-resolutions-bot-dev'
    source_file_path = 'construct_kb/data/llm_full_knowledge_base.json'
    destination_blob_name = 'data/llm_full_knowledge_base.json'

    upload_json_file_to_gcs(
        project_id, bucket_name, source_file_path, destination_blob_name
    )

    # create a RAG corpus
    display_name = 'csds-resolutions-bot-dev'
    embedding_model = 'publishers/google/models/text-embedding-005'
    rag_corpus = create_rag_corpus(project_id, display_name, embedding_model)
    print(f'RAG Corpus created: {rag_corpus.name}')
    # import files to the RAG corpus
    paths = [f'gs://{bucket_name}/{destination_blob_name}']
    import_files_to_rag_corpus(rag_corpus, paths)
    print(f'Files imported to RAG Corpus: {rag_corpus.name}')

    # retrieve a response
    response = _retrieve_response(rag_corpus)
    print(f'Response: {response}')
