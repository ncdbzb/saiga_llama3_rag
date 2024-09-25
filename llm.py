import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from logs.console_logger import console_logger

class LLM:
    def __init__(self, model_name="IlyaGusev/saiga_llama3_8b"):
        self.model_name = model_name
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
