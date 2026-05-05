from scapy.all import rdpcap
from scapy.layers.inet import TCP, UDP, IP
import numpy as np


def extract_features(pcap_file):
    packets = rdpcap(pcap_file)

    total_packets = len(packets)
    if total_packets == 0:
        return None


    packet_sizes = [len(pkt) for pkt in packets]

    avg_packet_size = np.mean(packet_sizes)
    max_packet_size = np.max(packet_sizes)
    min_packet_size = np.min(packet_sizes)
    total_bytes = np.sum(packet_sizes)
    std_packet_size = np.std(packet_sizes)


    timestamps = [float(pkt.time) for pkt in packets]

    duration = timestamps[-1] - timestamps[0] if total_packets > 1 else 0

    time_diffs = [
        timestamps[i] - timestamps[i - 1]
        for i in range(1, len(timestamps))
    ]

    avg_time_between = np.mean(time_diffs) if time_diffs else 0
    std_time_between = np.std(time_diffs) if time_diffs else 0


    tcp_count = 0
    udp_count = 0

    for pkt in packets:
        if pkt.haslayer(TCP):
            tcp_count += 1
        elif pkt.haslayer(UDP):
            udp_count += 1

    tcp_ratio = tcp_count / total_packets
    udp_ratio = udp_count / total_packets


    src_ip = packets[0][IP].src if packets[0].haslayer(IP) else None

    outgoing_packets = 0
    incoming_packets = 0

    for pkt in packets:
        if pkt.haslayer(IP):
            if pkt[IP].src == src_ip:
                outgoing_packets += 1
            else:
                incoming_packets += 1

    outgoing_ratio = outgoing_packets / total_packets
    incoming_ratio = incoming_packets / total_packets


    large_packets = [size for size in packet_sizes if size > 1000]
    small_packets = [size for size in packet_sizes if size < 200]

    large_packet_ratio = len(large_packets) / total_packets
    small_packet_ratio = len(small_packets) / total_packets


    features = {
        "total_packets": total_packets,
        "total_bytes": total_bytes,

        "avg_packet_size": avg_packet_size,
        "std_packet_size": std_packet_size,
        "max_packet_size": max_packet_size,
        "min_packet_size": min_packet_size,

        "duration": duration,
        "avg_time_between_packets": avg_time_between,
        "std_time_between_packets": std_time_between,

        "tcp_ratio": tcp_ratio,
        "udp_ratio": udp_ratio,

        "outgoing_ratio": outgoing_ratio,
        "incoming_ratio": incoming_ratio,

        "large_packet_ratio": large_packet_ratio,
        "small_packet_ratio": small_packet_ratio
    }

    return features