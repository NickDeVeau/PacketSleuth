# src/ai/build_dataset.py
"""
Parse .pcap files into JSONL dataset for AI training.
"""

import scapy.all as scapy
import pathlib
import json
import sys

def pcap_to_jsonl(pcap_path: str, label: str, out_file: str):
    packets = scapy.rdpcap(pcap_path)
    with open(out_file, "a") as f:
        for pkt in packets:
            features = {
                "src": pkt[0][1].src if pkt.haslayer(1) else "unknown",
                "dst": pkt[0][1].dst if pkt.haslayer(1) else "unknown",
                "proto": pkt[0].name,
                "len": len(pkt),
                "label": label
            }
            f.write(json.dumps(features) + "\n")

def main():
    if len(sys.argv) != 4:
        print("Usage: python build_dataset.py <pcap_path> <label> <out_file>")
        sys.exit(1)

    pcap_path, label, out_file = sys.argv[1:]
    pcap_to_jsonl(pcap_path, label, out_file)
    print(f"[+] Parsed {pcap_path} -> {out_file} (label={label})")

if __name__ == "__main__":
    main()
