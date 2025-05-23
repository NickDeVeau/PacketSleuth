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
sudo make capture-normal          # 10 s capture → data/normal_<ts>.pcap
```

*During those 10 seconds, browse* `https://example.com` *on **your Mac**.*

### 4 .2 Attack (poisoned) traffic

```bash
sudo make attack

# Victim device: browse http://neverssl.com  (plain HTTP)
sudo make capture-attack 
```

---

## 5 . Building the AI Dataset

```bash
sudo python src/ai/build_dataset.py data/normal.pcap normal  data/jsonl/normal.jsonl
sudo python src/ai/build_dataset.py data/attack.pcap attack  data/jsonl/attack.jsonl
```

---

## 6 . Training TinyBERT

```bash
sudo python src/ai/train.py
```

Model saved to `models/tinybert-pkt/` (ignored by git).

---

## 7 . Live Packet Classification

```bash
python src/ai/live_detect.py
```

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

### Author

Nick Deveau · 2025
```


