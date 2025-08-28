import os
from datasets import Dataset
from transformers import PreTrainedTokenizer

def load_dataset(file_path: str, tokenizer: PreTrainedTokenizer, block_size: int):
    # Fayldan matn o‘qish
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Tokenlarga ajratish
    tokens = tokenizer(
        text,
        return_special_tokens_mask=False,
        return_attention_mask=False,
        truncation=False
    )["input_ids"]

    # Bloklarga bo‘lish
    blocks = [tokens[i:i+block_size] for i in range(0, len(tokens) - block_size, block_size)]

    # Model uchun kerakli format
    examples = [{"input_ids": block, "labels": block.copy()} for block in blocks]

    return Dataset.from_list(examples)
