import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from logs.console_logger import console_logger

class LLM:
    def __init__(self, llm_name):
        self.model_name = llm_name
        # DEFAULT_SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            load_in_8bit=True,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        ).eval()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.generation_config = GenerationConfig.from_pretrained(self.model_name)
        print(console_logger.info(f'generation config:\n{self.generation_config}'))

    def call(self, prompt):
        # Генерация ответа с помощью модели
        data = self.tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
        data = {k: v.to(self.model.device) for k, v in data.items()}
        output_ids = self.model.generate(**data, generation_config=self.generation_config)[0]
        output_ids = output_ids[len(data["input_ids"][0]):]  # Убираем токены промпта
        output = self.tokenizer.decode(output_ids, skip_special_tokens=True).strip()

        return output
