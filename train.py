import json
import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import get_peft_model, LoraConfig, TaskType
from dataset import load_dataset

# ========== Konfiguratsiyani o‘qish ==========
with open("config.json") as f:
    config = json.load(f)

model_name = config["model_name"]
block_size = config["block_size"]
batch_size = config["batch_size"]
gradient_accumulation = config["gradient_accumulation"]
epochs = config["epochs"]
learning_rate = config["learning_rate"]
output_dir = config["output_dir"]

# ========== Modelni yuklash (to‘g‘ridan-to‘g‘ri CPUga) ==========
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
    attn_implementation="eager"  # Gemma uchun
).to("cpu")  # ← CPUda ishlaydi

# ========== Tokenizer ==========
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.padding_side = "right"
tokenizer.pad_token = tokenizer.eos_token

# ========== LoRA sozlamalari ==========
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Agar avval qo‘shilmagan bo‘lsa, LoRA ni qo‘shamiz
if not hasattr(model, "peft_config"):
    model = get_peft_model(model, lora_config)

# ========== Datasetni yuklash ==========
dataset = load_dataset("dataset/wikpedia.txt", tokenizer, block_size)

# ========== Trening argumentlari ==========
training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,
    num_train_epochs=epochs,
    per_device_train_batch_size=batch_size,
    gradient_accumulation_steps=gradient_accumulation,
    save_steps=100,
    save_total_limit=2,
    logging_steps=10,
    fp16=False,  # CPU bo‘lsa False
    learning_rate=learning_rate,
    remove_unused_columns=False,  # ← SHART!
    report_to="none"
)

# ========== Data collator ==========
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# ========== Trainer ==========
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator
)

# ========== Treningni boshlash ==========
trainer.train()

# ========== Model va tokenizerni saqlash ==========
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
