from scapy.all import rdpcap

packets = rdpcap("data/attack.pcap")
packets.summary()
