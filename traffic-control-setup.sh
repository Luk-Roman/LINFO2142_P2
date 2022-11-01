#!/bin/bash

TC=/sbin/tc

IF=lo

LIMIT=100mbit

DST_CIDR=127.0.0.1/32

U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"

create () {
  echo "== SHAPING INIT =="

  $TC qdisc add dev $IF root handle 1:0 htb \
    default 30

  $TC class add dev $IF parent 1:0 classid \
    1:1 htb rate $LIMIT

  $U32  match ip dst $DST_CIDR flowid 1:1

  echo "== SHAPING DONE =="
}

clean () {
  echo "== CLEAN INIT =="
  $TC qdisc del dev $IF root
  echo "== CLEAN DONE =="
}

clean
create