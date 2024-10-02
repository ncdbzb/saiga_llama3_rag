import time
from chroma_db import ChromaDB
# from llm import LLM
from prompt import get_prompt
from logs.console_logger import console_logger


LLM_NAME = "IlyaGusev/saiga_llama3_8b"
# Existing collections: "datapk_2_1_rubert_tiny_turbo"
COLLECTION_NAME = "datapk_2_1_rubert_tiny_turbo"  #WITHOUT EXTENSION
EMBEDDING_MODEL_NAME = "sergeyzh/rubert-tiny-turbo"
CHUNK_SIZE = 800
TOP_K = 4


def get_rag_response(user_query):
    # Ищем релевантные чанки
    chroma_db = ChromaDB(EMBEDDING_MODEL_NAME, CHUNK_SIZE)
    retrieved_chunks = chroma_db.similarity_search(COLLECTION_NAME, user_query, top_k=TOP_K)

    # Создаем промпт с найденным контекстом
    prompt = get_prompt(user_query, retrieved_chunks)

    #Делаем запрос к LLM
    # llm = LLM(LLM_NAME)
    # response = llm.call(prompt)

    return prompt

if __name__ == '__main__':
    print("App started. Введите 'exit' для завершения.")
    print(f'embedding model: {EMBEDDING_MODEL_NAME}')
    print(f'collection name: {COLLECTION_NAME}')

    while True:
        query = input("Введите ваш вопрос: ")

        if query.lower() in ['exit', 'quit', 'q']:
            print("Завершение работы приложения.")
            break

        start_time = time.time()

        # Получаем ответ от LLM (RAG)
        answer = get_rag_response(query)

        console_logger.info(f'Time: {time.time() - start_time}')

        print(f"Ответ: {answer}\n\n")
