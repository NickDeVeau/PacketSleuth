# src/defense/pinning_client.py
"""
Connects to server, verifies SSL cert fingerprint manually (SSL pinning).
"""

import ssl
import socket
import hashlib

# --- config ---
SERVER_HOST = "localhost"
SERVER_PORT = 4443

# This is the *expected* certificate fingerprint (SHA256 hex)
# We'll set this after first connection.
EXPECTED_FINGERPRINT = "731951045fb699fbdd6814e2290f65339f06b85d8de767a4a9a64d08c3a20176"

def get_cert_fingerprint(host: str, port: int) -> str:
    """Connects, retrieves cert, returns SHA256 fingerprint."""
    conn = socket.create_connection((host, port))
    context = ssl._create_unverified_context()   # <-- changed here
    sock = context.wrap_socket(conn, server_hostname=host)

    der_cert = sock.getpeercert(binary_form=True)
    sha256 = hashlib.sha256(der_cert).hexdigest()
    sock.close()
    return sha256

def main():
    actual_fp = get_cert_fingerprint(SERVER_HOST, SERVER_PORT)
    print(f"Server cert fingerprint:\n{actual_fp}")

    if EXPECTED_FINGERPRINT == "":
        print("[!] No fingerprint set yet. Copy this value into the script and retry.")
    elif actual_fp.lower() != EXPECTED_FINGERPRINT.lower():
        print("[!] WARNING: Certificate mismatch! Possible MITM attack!")
    else:
        print("[+] Certificate matches expected fingerprint. Secure connection.")

if __name__ == "__main__":
    main()
