# Authors : Jean-Christophe Bauduin & Lucas Roman - UCLouvain Belgium

import os
import pyshark
from glom import glom

# Change these parameters to modify the behaviour of the filter
# Remember to clean the qdisc with this function if you want to modify the limit :
# $ sudo tc qdisc del dev [interface] root

interface = "wlp1s0"
limit = "1mbit"
server_name = "nflxvideo"

print("Live capture starting ..")

capture = pyshark.LiveCapture(interface=interface, display_filter="ssl.handshake.extensions_server_name")
for packet in capture.sniff_continuously():
    sni = "0"
    protocol = "tcp"
    if "ssl" in packet:
        sni = glom(packet, "ssl.handshake_extensions_server_name")
    elif "tls" in packet:
        sni = glom(packet, "tls.handshake_extensions_server_name")
    elif "quic" in packet:
        sni = glom(packet, "quic.tls_handshake_extensions_server_name")
        protocol = "udp"
    else:
        continue
    ip = "0"
    if "ip" in packet:
        ip = packet["ip"]
    elif "ipv6" in packet:
        ip = packet["ipv6"]
    else:
        continue
    tcp = packet[protocol]
    print(sni)
    print("source:", ip.src, ":", tcp.srcport, "|", "destination:", ip.dst, ":", tcp.dstport)
    if server_name in sni:
        print(server_name + " detected, blocking")
        os.popen("./filter_setup.sh " + interface + " " + ip.dst + " " + limit)
    print("------------------------------------------------------------------")
