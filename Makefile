# PacketSleuth Makefile

.PHONY: capture attack defend pin-client

capture:
	@echo "[*] Starting 10-second capture on en0..."
	sudo python src/capture/record.py 10 en0

attack:
	@echo "[*] Launching Ettercap MITM attack..."
	./src/attack/run_ettercap.sh 192.168.1.231

defend:
	@echo "[*] Launching Flask HTTPS server with HSTS..."
	python src/defense/server.py

pin-client:
	@echo "[*] Running SSL-pinning client..."
	python src/defense/pinning_client.py
