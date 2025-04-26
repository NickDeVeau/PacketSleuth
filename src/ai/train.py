# src/ai/train.py
"""
Finetune TinyBERT on PacketSleuth traffic dataset.
"""

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch

# --- config ---
model_name = "huawei-noah/TinyBERT_General_4L_312D"
train_file = "data/jsonl/train.jsonl"
model_dir = "models/packet_detector"

def main():
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    dataset = load_dataset("json", data_files={"train": train_file})["train"]

    def tokenize_batch(batch):
        features = f"{batch['src']} {batch['dst']} {batch['proto']} {batch['len']}"
        return tokenizer(features, padding="max_length", truncation=True)

    dataset = dataset.map(tokenize_batch)
    dataset = dataset.rename_column("label", "labels")
    dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

    training_args = TrainingArguments(
        output_dir="./models/",
        evaluation_strategy="no",
        num_train_epochs=3,
        per_device_train_batch_size=32,
        logging_steps=10,
        save_strategy="epoch",
        learning_rate=2e-5,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    trainer.train()
    model.save_pretrained(model_dir)
    print(f"[+] Model saved to {model_dir}")

if __name__ == "__main__":
    main()
