"""
tshark wrapper: capture packets to PacketSleuth/data/<label>.pcap

Usage examples
--------------
# capture 10 s of clean traffic on default Wi-Fi (en0)
python src/capture/record.py 10 en0 normal

# capture 15 s of MITM traffic while Ettercap is running
python src/capture/record.py 15 en0 attack
"""
from __future__ import annotations
import subprocess
import pathlib
import datetime
import sys


def main() -> None:
    # ---------------------------------------------------------------- args ---
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 10      # seconds
    iface    = sys.argv[2] if len(sys.argv) > 2 else "en0"        # name or index
    label    = sys.argv[3] if len(sys.argv) > 3 else "normal"     # file label

    # -------------------------------------------------------------- paths ---
    root    = pathlib.Path(__file__).resolve().parents[2]         # PacketSleuth/
    out_dir = root / "data"
    out_dir.mkdir(exist_ok=True)

    ts      = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = out_dir / f"{label}.pcap"

    # ----------------------------------------------------------- run tshark ---
    cmd = ["tshark", "-i", str(iface), "-a", f"duration:{duration}", "-w", str(outfile)]
    print("Running:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print("✅  Saved to", outfile)
    except subprocess.CalledProcessError as e:
        print("❌  tshark exited with", e.returncode)
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
