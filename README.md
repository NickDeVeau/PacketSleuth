# PacketSleuth

🔎 Full MITM attack, prevention, and AI detection system.

---

## Features

- Capture real network traffic (tshark)
- Perform MITM attack (Ettercap ARP poisoning)
- Enforce HTTPS protection (Flask server with HSTS headers)
- Detect forged certificates (SSL pinning client)
- Train TinyBERT model on packets (HuggingFace Transformers)
- Live predict malicious vs normal traffic

---

## Project Structure

```
PacketSleuth/
├── src/
│   ├── capture/          # tshark recording
│   ├── attack/           # Ettercap scripts
│   ├── defense/          # HSTS Flask server & SSL pinning client
│   └── ai/               # Dataset creation, training, live detection
├── data/                 # .pcap captures + jsonl data
├── models/               # (ignored) trained models
├── certs/                # self-signed HTTPS certs
├── Makefile
├── requirements.txt
└── README.md
```

---

## Setup (One-time)

```bash
# 1. Clone repo
git clone <your_repo_url> PacketSleuth
cd PacketSleuth

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install system tools (Wireshark + Ettercap + Burp Suite)
brew install wireshark ettercap burp-suite-community
```

🔵 **Note:** Accept permission prompts for packet capture if Wireshark asks.

---

## Usage (Development & Testing)

### Traffic Capture

```bash
make capture
```
- Captures 10 seconds of live traffic from interface `en0`.
- Saved as `data/YYYYMMDD_HHMMSS.pcap`.

🔵 May require `sudo` if not a member of `access_bpf` group.

---

### MITM Attack (ARP Poisoning)

```bash
# Edit victim IP manually inside src/attack/run_ettercap.sh
make attack
```
- Launches Ettercap in ARP poisoning mode.
- Victim traffic will relay through attacker (your Mac).

---

### Defense Server (HTTPS + HSTS)

```bash
make defend
```
- Runs Flask HTTPS server at `https://localhost:4443`.
- Forces HSTS headers to block HTTPS downgrade.

Visit:
```
https://localhost:4443
```
🔵 Browser will warn about "Self-signed Certificate" — expected.

---

### SSL Pinning Client

```bash
make pin-client
```
- Connects to server, verifies SSL certificate fingerprint.
- Rejects altered/fake certificates (MITM prevention).

---

## AI Pipeline (Training + Live Prediction)

### Step 1: Build JSONL Dataset from PCAP

```bash
python src/ai/build_dataset.py <path-to-pcap> <label> <output-jsonl>
```
Example:

```bash
python src/ai/build_dataset.py data/20250425_XXXXXX.pcap normal data/jsonl/normal.jsonl
python src/ai/build_dataset.py data/ettercap_session.pcap attack data/jsonl/attack.jsonl
```

---

### Step 2: Train TinyBERT Model

```bash
python src/ai/train.py
```
- Fine-tunes TinyBERT on your packet data.
- Saves model into `models/tinybert-pkt/` (ignored by git).

---

### Step 3: Live Predict Packet Flows

```bash
python src/ai/live_detect.py
```
- Manually type `src dst proto len`
- Model predicts `NORMAL` or `ATTACK`.

Example:

```
192.168.1.5 192.168.1.1 TCP 60
```

---

## Notes

- Everything runs **natively** on macOS — **no VMs** needed.
- Ettercap traffic can be viewed via Burp Suite proxy (port 8080).
- If no packets are captured, check correct interface with:
  ```bash
  tshark -D
  ```

---

## Authors

Nick Deveau — 2025
```

---

✅ **Clear, precise, actionable.**

### 📋 Commands now cover:

- Clone
- venv
- pip install
- brew install
- make capture/attack/defend/pin-client
- pcap parsing
- TinyBERT training
- Live packet detection

---

### 📥 After copy-pasting:

```bash
git add README.md
git commit -m "docs: finalized README with full step-by-step commands"
git push
```

