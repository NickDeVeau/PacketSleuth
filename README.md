# PacketSleuth

🔎 A complete MITM attack + defense + AI detection system.

---

## Features

- Capture real packets (tshark)
- Perform MITM attack (Ettercap: ARP poisoning + sslstrip prep)
- Defend with HSTS (Flask HTTPS server)
- Detect MITM via SSL pinning (Python client)
- Train TinyBERT model on packet flows (HuggingFace)
- Live classify packets as "normal" or "attack"

---

## Project Structure

```
PacketSleuth/
├── src/
│   ├── capture/          # Packet recording (tshark wrapper)
│   ├── attack/           # Ettercap MITM runner scripts
│   ├── defense/          # Flask server + SSL pinning client
│   └── ai/               # Dataset builder, trainer, live detection
├── data/                 # .pcap captures and jsonl files
├── models/               # (ignored) trained TinyBERT model
├── certs/                # Self-signed certs for HTTPS
├── requirements.txt
├── Makefile
└── README.md
```

---

## Usage

### Setup

```bash
# clone
git clone <repo>
cd PacketSleuth

# create venv
python3 -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt
brew install wireshark ettercap burp-suite-community
```

---

### Run Targets

```bash
make capture       # record clean traffic (baseline)
make attack        # run Ettercap MITM (edit victim IP first)
make defend        # launch HTTPS+HSTS server
make pin-client    # SSL pinning client connects
```

---

### AI Pipeline

```bash
# create JSONL dataset
python src/ai/build_dataset.py <path-to-pcap> <label> <output.jsonl>

# train TinyBERT
python src/ai/train.py

# live packet detection
python src/ai/live_detect.py
```

---

## Notes

- No VMs needed — native macOS
- After MITM starts, intercepted credentials can be seen via Burp Suite Proxy
- Defense server forces HSTS headers to block downgrade attacks
- SSL pinning client refuses to connect if a fake cert is injected

---

## Authors

Nick Deveau — 2025
```
