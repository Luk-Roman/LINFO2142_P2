#!/bin/bash


# Usage : sudo ./traffic-control-setup.sh [interface] [destination ip] [destination port] [source port]

TC=/sbin/tc

IF=$1

LIMIT=50mbit # Il faut trouver une solution pour le doser un peu mieux

DST_IP=$2
DST_PORT=$3
SRC_PORT=$4

U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"

create () {
  SHOW=$(tc qdisc show dev "$IF")
  EMPTY="qdisc pfifo_fast 0: root refcnt 2 bands 3 priomap 1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1"

  if  [[ $SHOW == "$EMPTY"* ]] ; then
    echo "No qdisc on "$IF" : creating one ..."
    $TC qdisc replace dev $IF root handle 1:0 htb \
      default 30

    $TC class replace dev $IF parent 1:0 classid \
      1:1 htb rate $LIMIT
  fi
  $U32 \
    match ip src $DST_IP \
    match ip sport $DST_PORT 0xffff \
    match ip dport $SRC_PORT 0xffff \
    flowid 1:1

}

# clean () {
#   $TC qdisc del dev $IF root 2>/dev/null
# }

# clean
create
echo "Done !"
