#!/bin/bash


# Usage : sudo ./traffic-control-setup.sh [interface] [destination ip] [destination port] [source port]

TC=/sbin/tc

IF=$1

LIMIT=1mbit

DST_IP=$2
DST_PORT=$3
SRC_PORT=$4

U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"

create () {

  $TC qdisc add dev $IF root handle 1:0 htb \
    default 30

  $TC class add dev $IF parent 1:0 classid \
    1:1 htb rate $LIMIT

  $U32 \
    match ip dst $DST_IP \
    match ip dport $DST_PORT 0xffff \
    match ip sport $SRC_PORT 0xffff \
    flowid 1:1

}

clean () {
  $TC qdisc del dev $IF root 2>/dev/null
}

clean
create
echo "Done !"