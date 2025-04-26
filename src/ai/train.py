"""
Finetune TinyBERT on PacketSleuth dataset.
- Reads *.jsonl from data/jsonl/
- Splits 90 % train / 10 % eval
- Saves model to models/tinybert-pkt

Requires:
    pip install torch>=2.3.0 transformers>=4.40 datasets>=2.19 scikit-learn
"""

import pathlib, random, json
from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch

MODEL_NAME = "huawei-noah/TinyBERT_General_4L_312D"
DATA_DIR   = pathlib.Path("data/jsonl")
OUT_DIR    = pathlib.Path("models/tinybert-pkt")

def load_packet_ds():
    paths = list(DATA_DIR.glob("*.jsonl"))
    if not paths:
        raise ValueError(f"No JSONL files found in {DATA_DIR}")
    
    raw = load_dataset("json", data_files=[str(p) for p in paths], split="train")

    # build "text" field + label (binary)
    def join_fields(row):
        row["text"]  = f'{row["src"]} {row["dst"]} {row["proto"]} {row["len"]}'
        row["label"] = 1 if row["label"] == "attack" else 0
        return row

    raw = raw.map(join_fields)
    split = raw.train_test_split(test_size=0.1, seed=42)
    return DatasetDict(train=split["train"], test=split["test"])

def tokenize(ds, tokenizer):
    return ds.map(lambda row: tokenizer(row["text"], truncation=True), batched=True)

def main():
    ds         = load_packet_ds()
    tokenizer  = AutoTokenizer.from_pretrained(MODEL_NAME)
    ds_tok     = tokenize(ds, tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=2
    )

    args = TrainingArguments(
        output_dir=str(OUT_DIR),
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        learning_rate=3e-5,
        save_strategy="no",
        report_to="none",
        seed=42,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=ds_tok["train"],
        eval_dataset=ds_tok["test"],
        tokenizer=tokenizer,
    )

    trainer.train()
    metrics = trainer.evaluate()
    print(metrics)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(OUT_DIR)
    tokenizer.save_pretrained(OUT_DIR)
    print(f"✔ Model saved to {OUT_DIR}")

    # --- Sample Inputs Logging ---
    print("\nSample inputs you can use in live_detect.py:")

    # Recover original train split for examples
    train_raw = ds["train"]

    # Show 3 NORMAL samples
    print("\n[NORMAL examples]")
    normal = [row["text"] for row in train_raw if row["label"] == 0]
    for example in normal[:3]:
        print(example)

    # Show 3 ATTACK samples
    print("\n[ATTACK examples]")
    attack = [row["text"] for row in train_raw if row["label"] == 1]
    for example in attack[:3]:
        print(example)

if __name__ == "__main__":
    torch.manual_seed(42)
    random.seed(42)
    main()
