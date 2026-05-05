from scapy.all import rdpcap
import numpy as np

MAX_LEN = 10000

def extract_sequence(pcap_file):
    packets = rdpcap(pcap_file)

    sequence = []


    first_ip = None
    for pkt in packets:
        if pkt.haslayer("IP"):
            first_ip = pkt["IP"].src
            break


    if first_ip is None:
        return np.zeros(MAX_LEN, dtype=int)


    for pkt in packets:
        if pkt.haslayer("IP"):
            if pkt["IP"].src == first_ip:
                sequence.append(1)
            else:
                sequence.append(-1)


    if len(sequence) > MAX_LEN:
        sequence = sequence[:MAX_LEN]
    else:
        sequence.extend([0] * (MAX_LEN - len(sequence)))

    return np.array(sequence, dtype=int)