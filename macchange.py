#! /usr/bin/python

import subprocess
from termcolor import colored

def change_mac_address(interface, mac):
	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", mac])
	subprocess.call(["ifconfig", interface, "up"])

def main():
	interface = input("[*] Enter Interface To Change Mac Address On: ")
	new_mac = input("[*] Enter Mac Address To Change To: ")

	before_change = subprocess.check_output(["ifconfig", interface])
	change_mac_address(interface, new_mac)
	after_change = subprocess.check_output(["ifconfig", interface])

	if before_change == after_change:
		print(colored("[!!] Failed To Change MAC Address to " + new_mac, "red"))
	else:
		print(colored("[+] MAC Address Changed To " + new_mac, "green"))

if __name__ == "__main__":
	main()
