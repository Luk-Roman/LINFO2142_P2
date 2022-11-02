import pyshark, os
from glom import glom
interface= "wlan0"
capture = pyshark.LiveCapture(interface=interface,display_filter="ssl.handshake.extensions_server_name")
for packet in capture.sniff_continuously():
  #print(packet)
  sni="0"
  protocol="tcp"
  if("ssl" in packet):
    sni = glom(packet,"ssl.handshake_extensions_server_name")
  elif("tls" in packet):
    sni = glom(packet,"tls.handshake_extensions_server_name")
  elif("quic" in packet):
    sni = glom(packet,"quic.tls_handshake_extensions_server_name")
    protocol = "udp"
  else:
    continue
  ip="0"
  if("ip" in packet):
    ip=packet["ip"]
  elif("ipv6" in packet):
    ip=packet["ipv6"]
  else:
    continue
  tcp = packet[protocol]
  print(sni)
  print("source:",ip.src,":",tcp.srcport,"|","destination:",ip.dst,":",tcp.dstport)
  if("googlevideo" in sni):
    print("youtube detected, blocking")
    os.popen("./traffic-control-setup.sh "+interface+" "+ip.dst+" "+tcp.dstport+" "+tcp.srcport)
  print("------------------------------------------------------------------")

