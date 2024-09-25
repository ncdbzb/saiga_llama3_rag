import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
from logs.console_logger import console_logger


class ChromaDB:
    def __init__(self, embedding_model_name):
        self.persist_directory = os.path.join('data', 'chroma')
        self.client = chromadb.PersistentClient(self.persist_directory)

        class LocalHuggingFaceEmbeddingFunction(EmbeddingFunction[Documents]):
            def __call__(self, input_docs: Documents) -> Embeddings:
                embedding_model = SentenceTransformer(embedding_model_name)
                return embedding_model.encode(input_docs).tolist()

        self.custom_ef = LocalHuggingFaceEmbeddingFunction()

    def _get_or_create_collection(self, collection_name):
        if collection_name in self.client.list_collections():
            collection = self.client.get_collection(collection_name)
        else:
            console_logger.warning(f'No collection "{collection_name}" in {self.persist_directory}')
            if any(os.path.splitext(file)[0] == collection_name for file in os.listdir(self.persist_directory)):
                console_logger.warning(f'Creating collection"{collection_name}" in {self.persist_directory}')
                collection = self.client.create_collection(name=collection_name, embedding_function=self.custom_ef)


        # Добавляем чанки в коллекцию
        chunk_ids = [str(i) for i in range(len(chunks))]
        collection.add(documents=chunks, ids=chunk_ids)


    def similarity_search(collection, user_query, n_results=4):
        results = collection.query(query_texts=[user_query], n_results=n_results)
        return results['documents'][0]
