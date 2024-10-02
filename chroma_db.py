import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer
from logs.console_logger import console_logger
from scraping.dita_parser import parse_dita
from scraping.txt_parser import parse_txt
from scraping.text_splitter import split_text
from semantic_text_splitter import TextSplitter


class ChromaDB:
    def __init__(self, embedding_model_name, chunk_size):
        self.persist_directory = os.path.join('data', 'chroma')
        self.client = chromadb.PersistentClient(self.persist_directory)
        self.chunk_size = chunk_size

        class LocalHuggingFaceEmbeddingFunction(EmbeddingFunction[Documents]):
            def __call__(self, input_docs: Documents) -> Embeddings:
                embedding_model = SentenceTransformer(embedding_model_name)
                return embedding_model.encode(input_docs).tolist()

        self.custom_ef = LocalHuggingFaceEmbeddingFunction()

    def _get_or_create_collection(self, collection_name):
        if collection_name in self.get_list_collections():
            collection = self.client.get_collection(name=collection_name, embedding_function=self.custom_ef)
        else:
            console_logger.warning(f'No collection "{collection_name}" in {self.persist_directory}')
            ext = None
            for file in os.listdir(os.path.join('data', 'docs')):
                if os.path.splitext(file)[0] == collection_name:
                    ext = os.path.splitext(file)[-1]
            if ext:
                file_path = os.path.join('data', 'docs', f'{collection_name}{ext}')
                if ext == '.zip':
                    parsed_content = parse_dita(file_path)
                elif ext == '.txt':
                    parsed_content = parse_txt(file_path)
                else:
                    raise ValueError(f'Unexpected extension: {ext}')
                splitter = TextSplitter(self.chunk_size)
                chunks = splitter.chunks(parsed_content)
                console_logger.info(f'Creating collection "{collection_name}" in {self.persist_directory}')
                collection = self.client.create_collection(name=collection_name, embedding_function=self.custom_ef)

                # Добавляем чанки в коллекцию
                chunk_ids = [str(i) for i in range(len(chunks))]
                collection.add(documents=chunks, ids=chunk_ids)
                console_logger.info(f'Collection "{collection_name}" was created in {self.persist_directory} with chunk_size={self.chunk_size}')
            else:
                console_logger.warning(f'No document "{collection_name}" in {os.path.join("data", "docs")}')
                return
        return collection

    def similarity_search(self, collection_name, user_query, top_k=4):
        collection = self._get_or_create_collection(collection_name)

        if not collection:
            raise ValueError(f"Collection {collection_name} was not found")

        results = collection.query(query_texts=[user_query], n_results=top_k)
        console_logger.info(f'Distances: {results["distances"][0]}')
        docs = results['documents'][0]
        return '\n\n'.join(docs)

    def get_list_collections(self):
        list_collections = self.client.list_collections()
        return list(map(lambda x: x.name, list_collections))
