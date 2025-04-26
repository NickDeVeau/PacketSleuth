# PacketSleuth  
Man-in-the-Middle attack · counter-measures · AI-based traffic detection
-----------------------------------------------------------------------

## 1 . Project Overview
PacketSleuth captures network packets, demonstrates an Ettercap MITM attack, blocks it with HSTS + SSL pinning, then trains a TinyBERT model to label traffic as **NORMAL** vs **ATTACK**.

---

## 2 . Repository Layout
```
PacketSleuth/
├── src/
│   ├── capture/        # tshark recorder
│   ├── attack/         # Ettercap runner + helpers
│   ├── defense/        # Flask HTTPS server + pinning client
│   └── ai/             # dataset builder, TinyBERT trainer, live detect
├── data/               # PCAP & JSONL files
├── certs/              # self-signed HTTPS certs
├── models/             # (git-ignored) trained models
├── Makefile            # one-touch commands
├── requirements.txt
└── README.md
```

---

## 3 . Quick Setup (macOS)

```bash
git clone <repo> PacketSleuth
cd PacketSleuth
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
brew install wireshark ettercap burp-suite-community
```

> **Tip :** if Wireshark asks about `ChmodBPF`, choose **YES** so you can capture without `sudo`.

---

## 4 . Capturing Traffic

### 4 .1 Normal (clean) traffic

```bash
make capture-normal          # 10 s capture → data/normal_<ts>.pcap
```

*During those 10 seconds, browse* `https://example.com` *on **your Mac**.*

### 4 .2 Attack (poisoned) traffic

```bash
make attack                  # terminal 1 – start Ettercap (leave running)

# Victim device: browse http://neverssl.com  (plain HTTP)
make capture-attack          # terminal 2 – 10 s capture → data/attack_<ts>.pcap
```

---

## 5 . Building the AI Dataset

```bash
mkdir -p data/jsonl
python src/ai/build_dataset.py data/normal_*.pcap normal  data/jsonl/normal.jsonl
python src/ai/build_dataset.py data/attack_*.pcap attack  data/jsonl/attack.jsonl
```

---

## 6 . Training TinyBERT

```bash
python src/ai/train.py       # ~1–2 min on CPU
```

Model saved to `models/tinybert-pkt/` (ignored by git).

---

## 7 . Live Packet Classification

```bash
python src/ai/live_detect.py
```

| Example input (`src dst proto len`) | Expected output |
|-------------------------------------|-----------------|
| `192.168.1.76 192.168.1.1 TCP 60`   | **NORMAL** |
| `10.0.0.5 224.0.0.251 UDP 93`       | **ATTACK** |
| `192.168.1.231 192.168.1.254 TCP 512` | **ATTACK** |
| `192.168.1.76 192.168.1.1 TCP 52`   | **NORMAL** |

*(These mimic patterns the model saw during training; use them during your demo.)*

Type `q` to quit the live prompt.

---

## 8 . Defense Components

| Command | Description |
|---------|-------------|
| `make defend`      | Launch Flask HTTPS server on `https://localhost:4443` (sends HSTS). |
| `make pin-client`  | Client connects and checks SHA-256 cert fingerprint. <br>Outputs **“Certificate matches”** (normal) or **warning** (fake cert / MITM). |

---

## 9 . MITM Attack Controls

| Command | Description |
|---------|-------------|
| `make attack` | Ettercap ARP-poisons `<victim IP>` ↔ gateway and logs to `data/ettercap_session.pcap`. <br>Press **`v`** inside Ettercap to cycle visual modes; press **Space** to pause/resume; **q** to quit. |

> **How do I know the attack is active?**  
> Ettercap prints **“ARP poisoning victims”** followed by both IPs and begins showing UDP/TCP events.  
> Optionally open Wireshark on `en0` to see ARP replies flooding the LAN.

---

## 10 . Makefile Targets (complete list)

| Target | Action |
|--------|--------|
| `make capture-normal` | record 10 s clean traffic |
| `make capture-attack` | record 10 s while MITM is running |
| `make attack` | run Ettercap (needs victim IP inside script) |
| `make defend` | start HTTPS + HSTS server |
| `make pin-client` | run SSL-pinning check |

---

## 11 . Demo-video flow (2 min 30 s)

1. `make capture-normal` → file saved.  
2. `make attack` (terminal 1) + victim browses HTTP.  
3. `make capture-attack` (terminal 2) → second PCAP saved.  
4. Build dataset + train TinyBERT (fast forward in video).  
5. Run `live_detect.py`, type sample inputs, show **NORMAL / ATTACK** prints.  
6. Stop Ettercap → `make defend` → load `https://localhost:4443`.  
7. Run `make pin-client` → show *certificate matches*.

---

### Author

Nick Deveau · 2025
```


