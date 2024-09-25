


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def rag_with_chunks(query):
    # Ищем релевантные чанки
    retrieved_chunk = similarity_search(collection, query)

    # Создаем промпт с найденным контекстом
    prompt = get_prompt(query, retrieved_chunk)

    # Генерация ответа с помощью модели
    data = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
    data = {k: v.to(model.device) for k, v in data.items()}
    output_ids = model.generate(**data, generation_config=generation_config)[0]
    output_ids = output_ids[len(data["input_ids"][0]):]  # Убираем токены промпта
    output = tokenizer.decode(output_ids, skip_special_tokens=True).strip()

    return output

# Пример запроса
query = "Как осуществить установку и использование сервиса управления БД Adminer?"
answer = rag_with_chunks(query)
print(f"Ответ: {answer}")