#!/bin/bash
# src/attack/get_gateway_ip.sh
# Get the default IPv4 gateway on macOS cleanly

netstat -rn -f inet | awk '/^default/ {print $2; exit}'
