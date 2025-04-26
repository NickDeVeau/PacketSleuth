import scapy.all as scapy
import json
import sys

def build_dataset(pcap_file, label, output_file):
    packets = scapy.rdpcap(pcap_file)
    print(f"Loaded {len(packets)} packets")

    entries = []

    for pkt in packets:
        # Check if packet has IP layer
        if pkt.haslayer(scapy.IP):
            src_ip = pkt[scapy.IP].src
            dst_ip = pkt[scapy.IP].dst

            # Check if packet has TCP or UDP
            if pkt.haslayer(scapy.TCP):
                proto = "TCP"
            elif pkt.haslayer(scapy.UDP):
                proto = "UDP"
            else:
                proto = "IP"

            length = len(pkt)

            entry = {
                "src": src_ip,
                "dst": dst_ip,
                "proto": proto,
                "len": length,
                "label": label
            }
            entries.append(entry)

    # Write to output JSONL
    with open(output_file, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    print(f"Wrote {len(entries)} entries to {output_file}")

if __name__ == "__main__":
    pcap_file = sys.argv[1]
    label = sys.argv[2]
    output_file = sys.argv[3]
    build_dataset(pcap_file, label, output_file)
