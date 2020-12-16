#!/usr/bin/env python3.7

from netmiko import ConnectHandler
import time

with ConnectHandler(host="192.168.166.103", port=22, username="admin",password="Cisco123",device_type="cisco_xe") as ch:
    out = ch.send_command("ping 1.1.1.1 so loopback 0")
    out1= ch.send_command("ping 11.11.11.11 so loopback 1")
    print("Performing the ping from #{} to Pod_A_R1's loopback interfaces".format(ch.find_prompt()))
    print(out)
    print("\n\n\n\n")
    print(out1)