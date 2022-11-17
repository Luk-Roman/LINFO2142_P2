# Authors : Jean-Christophe Bauduin & Lucas Roman - UCLouvain Belgium

import math
import pyshark
from glom import glom

interface = "wlp1s0"
server_name = "nflxvideo"
capture_limit = 100
file1 = open("output.csv", "w")
file1.write("ip,payload_size,entropy\n")


print("Live capture starting ..")
def entropy(string): # source : https://security.stackexchange.com/questions/101098/entropy-on-payload
        prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
        entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
        return entropy

watched_ips = []
payloads = []
captured_cnt = 0
capture = pyshark.LiveCapture(interface=interface)
for packet in capture.sniff_continuously(): #packet_count=1000
    if captured_cnt == capture_limit:
        break
    try : #Handshake TLS/SSL
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
        if server_name in sni:
            if (ip.dst not in watched_ips):
                watched_ips.append(ip.dst)
    except : #Other
        if "ip" in packet:
            ip = packet["ip"]
        elif "ipv6" in packet:
            ip = packet["ipv6"]
        else:
            continue
        if(ip.src in watched_ips):
            try:
                payload = packet["TLS"].app_data
                length = packet["TLS"].record_length
                file1.write(ip.src+","+length+","+str(entropy(payload)))
                file1.write("\n")
                print("# of captured packets : "+str(captured_cnt)+"/"+str(capture_limit))
                captured_cnt+=1

            except:
                continue

print("# of captured packets : "+str(captured_cnt)+"/"+str(capture_limit))
file1.close()
