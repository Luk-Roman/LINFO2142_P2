# Purpose of the experiment :
#### As part of a course given by Professor O. Bonaventure (UCLouvain, Belgium), we were led to set up a network that does not respect net neutrality in order to test the [Wehe](https://dd.meddle.mobi/index.html) application.
#### For the experiment, we have set up a raspberry which creates a Wi-Fi hotspot. This repository contains the code to run if you want to reproduce our experiments and check our results.

## Files :
### filter_setup.sh
This bash script is used to set up the filtering method using the **tc** command which is available by default on most Linux distributions.
We create a classful **htb qdisc** on the specified interface. We then create a class, where we throttle the bandwidth to the specified limit.
Finally, we apply a u32 filter that matches the specified source ip and queue its traffic to our throttled class.

```bash
$ sudo ./filter_setup.sh [interface] [ip source] [limit]
```
To see what is the accepted limit format, please refer to [this man page](https://man7.org/linux/man-pages/man8/tc.8.html#PARAMETERS).

### server_throttling.py
This python script is used to capture the traffic and check the SNI during the SSL handshake. If the server name match our specified server name, we then apply a filter on this ip address to slow it down.
If you wish to change the parameters (interface, server name, or speed limit), you can modify the parameters at the top of the file.
```bash
$ sudo python server_throttling.py
```

## Remarks :
If you wish to flush the qdisc on a specific interface, you can run this command :
```bash
$ sudo tc qdisc delete dev [interface] root
```
## Dependencies :
In order for our python script to work you must install these two python libraries :
* [pyshark](https://pypi.org/project/pyshark/)
* [glom](https://pypi.org/project/glom/)

And you must install this package :
* [tshark](https://www.wireshark.org/docs/man-pages/tshark.html)
## Contact :
If you wish to contact us about our experiment, feel free to reach us by email :
* Jean-Christophe Bauduin - [jean-christophe.bauduin@student.uclouvain.be](mailto:jean-christophe.bauduin@student.uclouvain.be)
* Lucas Roman - [lucas.roman@student.uclouvain.be](mailto:lucas.roman@student.uclouvain.be)
