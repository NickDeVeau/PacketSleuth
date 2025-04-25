# src/capture/record.py
"""
tshark wrapper: capture packets to PacketSleuth/data/YYYYMMDD_HHMMSS.pcap

Usage:
    python -m capture.record 10       # capture for 10 seconds
"""
import subprocess, pathlib, datetime, sys

def main() -> None:
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    root = pathlib.Path(__file__).resolve().parents[2]   # PacketSleuth/
    out_dir = root / "data"
    out_dir.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = out_dir / f"{ts}.pcap"

    cmd = ["tshark", "-a", f"duration:{duration}", "-w", str(outfile)]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("Saved to", outfile)

if __name__ == "__main__":
    main()
