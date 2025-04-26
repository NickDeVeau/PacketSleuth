# src/ai/live_detect.py
"""
Live packet prediction using TinyBERT model.
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_DIR = "models/tinybert-pkt"

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

def predict(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    pred = torch.argmax(logits, dim=1).item()
    label = "attack" if pred == 1 else "normal"
    return label

if __name__ == "__main__":
    print("Live Packet Detection Ready.")
    while True:
        fake_packet = input("Enter 'src dst proto len' (or 'q' to quit): ").strip()
        if fake_packet.lower() == "q":
            break
        result = predict(fake_packet)
        print(f"Predicted: {result.upper()}")
