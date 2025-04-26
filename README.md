# PacketSleuth

Man-in-the-Middle Attack, Defense, and AI Detection System

---

## Overview

PacketSleuth captures network traffic, simulates MITM attacks, implements countermeasures, and uses a lightweight AI model to classify traffic as normal or malicious.

---

## Project Structure

```
PacketSleuth/
├── src/
│   ├── capture/        # Packet recording (tshark wrapper)
│   ├── attack/         # Ettercap MITM scripts
│   ├── defense/        # HSTS Flask server and SSL pinning client
│   └── ai/             # Dataset builder, TinyBERT trainer, live detection
├── data/               # PCAP and JSONL data
├── certs/              # Self-signed HTTPS certs
├── models/             # (ignored) trained models
├── Makefile
├── requirements.txt
└── README.md
```

---

## Setup Instructions

1. Clone the repository:

```bash
git clone <your_repo_url> PacketSleuth
cd PacketSleuth
```

2. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install system dependencies (macOS only):

```bash
brew install wireshark ettercap burp-suite-community
```

---

## How to Capture Traffic

### Capturing Normal Traffic (no attack)

```bash
make capture
```
- Captures 10 seconds of normal traffic from interface `en0`.
- Save the `.pcap` file for training as a "normal" example.

**Note:**  
If no packets are captured, use `tshark -D` to verify the correct interface.

---

### Capturing Attack Traffic (MITM)

1. Edit victim IP manually inside `src/attack/run_ettercap.sh` if needed.

2. Launch Ettercap attack:

```bash
make attack
```
- Runs ARP poisoning between victim and gateway.
- Traffic will flow through your machine.
- Save the resulting `ettercap_session.pcap` for training as an "attack" example.

---

## How to Train the AI Model

1. Convert PCAP files to JSONL format:

```bash
python src/ai/build_dataset.py data/<normal_capture>.pcap normal data/jsonl/normal.jsonl
python src/ai/build_dataset.py data/<attack_capture>.pcap attack data/jsonl/attack.jsonl
```

2. Train TinyBERT model:

```bash
python src/ai/train.py
```
- Model will be saved under `models/tinybert-pkt/`.

---

## How to Test and Predict

1. Run live packet detection manually:

```bash
python src/ai/live_detect.py
```

2. Enter packet information manually when prompted:

Example:

```
192.168.1.5 192.168.1.1 TCP 60
```

3. The model will classify the packet as either "NORMAL" or "ATTACK".

---

## Defense Scripts

### Launch HTTPS + HSTS Server

```bash
make defend
```
- Runs Flask HTTPS server on `https://localhost:4443`.
- Forces HSTS headers to prevent HTTPS downgrade attacks.

---

### Run SSL Pinning Client

```bash
make pin-client
```
- Connects to the server and checks SSL certificate fingerprint.
- Refuses connection if the certificate is altered (MITM protection).

---

## Notes

- Capturing packets (`make capture`) may require `sudo` privileges depending on system configuration.
- Make sure to open traffic in Wireshark or Burp Suite if you want to manually inspect MITM results.
- All commands assume you are inside an activated `.venv`.

---

## Author

Nick Deveau — 2025
```
