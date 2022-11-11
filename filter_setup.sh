#!/bin/bash

# Usage : sudo ./filter_setup.sh [interface] [destination ip] [limit]
# Example : sudo ./filter_setup.sh wlan0 8.8.8.8 10mbit
# Authors : Jean-Christophe Bauduin & Lucas Roman - UCLouvain Belgium

TC=/sbin/tc

IF=$1
SRC_IP=$2
LIMIT=$3


U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"

create () {
  SHOW=$(tc qdisc show dev "$IF")
  ALREADY_USED="qdisc htb 1: root refcnt 2 r2q 10 default 0x30"
  if  [[ $SHOW != "$ALREADY_USED"* ]] ; then # Checking if the qdisc has already been properly set up
    $TC qdisc replace dev "$IF" root handle 1:0 htb \
      default 30
    $TC class replace dev "$IF" parent 1:0 classid \
      1:1 htb rate "$LIMIT"
  fi

  $U32 match ip src "$SRC_IP" flowid 1:1

}

create
echo "Filter applied on interface $IF - throttling $SRC_IP to $LIMIT !"
