# Authors : Jean-Christophe Bauduin & Lucas Roman - UCLouvain Belgium

import os
import pyshark
from glom import glom

# Change these parameters to modify the behaviour of the filter
# Remember to clean the qdisc with this function if you want to modify the limit :
# $ sudo tc qdisc del dev [interface] root

interface = "wlan0"
limit = "1mbit"
server_name = "nflxvideo"

print("Live capture starting ..")

capture = pyshark.LiveCapture(interface=interface, display_filter="dns")
for pkt in capture.sniff_continuously():
    try:
        if server_name in pkt.dns.resp_name :
            if (int(pkt.dns.count_answers) > 0):
                try: #ipv6
                    print(pkt.dns.aaaa + " detected, blocking")
                    os.popen("./filter_setup.sh " + interface + " " + pkt.dns.aaaa + " " + limit)
                except:
                    pass
                try: #ipv4
                    print(pkt.dns.a + " detected, blocking")
                    os.popen("./filter_setup.sh " + interface + " " + pkt.dns.a + " " + limit)
                except:
                    pass
                print("------------------------------------------------------------------")
    except AttributeError as e:
        #ignore packets that aren't DNS Response
        pass