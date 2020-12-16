#!/usr/bin/env python3.7

from netmiko import ConnectHandler
import time

from rich import print
from rich.console import Console
from rich.table import Table

#Prepare the list of devices where config needs to be pushed
hosts = open("device-list.txt").read().split("\n")

#define an empty dictionary to store the Interface and OSPF operational data per host basis
intf = {}
ospf_n = {}
ospf_intf = {}

# establish an SSH connection with host and collect the operational details
for H in hosts:
    with ConnectHandler(host=H, port=22, username="admin",password="Cisco123",device_type="cisco_xe") as ch:
        intf[ch.find_prompt()] = ch.send_command("show ip interface brief")
        ospf_n[ch.find_prompt()] = ch.send_command("show ip ospf neighbor")
        ospf_intf[ch.find_prompt()]=ch.send_command('show ip ospf interface brief')
        
print("Interface and OSPF operational data is collected")

print("###########################\n###########################\n\n")
console = Console()
console.print("Printing the Interface status on each device", style= "bold white on magenta")
#print(intf,ospf_n,ospf_oper)
for items in intf:
    raw = intf[items].strip()
    raw_s = raw.split("\n")
    hdr = Table(show_header = True, header_style="bold black")
    hdr.add_column("Interface Name", width = 20)
    hdr.add_column("IP Address", width = 15)
    hdr.add_column("Enabled", width = 10)
    hdr.add_column("Status", width =10)
    console.print(items, style = "bold black on white")
    for i in range(1,len(raw_s)):
        data = raw_s[i].split()
        name = data[0]
        ip = data[1]
        if data[4] == "administratively":
            enabled = "Admin Down"
        else:
            enabled = data[4]
        status = data[5]
        hdr.add_row(name,ip,enabled,status)
    print(hdr)
    time.sleep(5)
    
print("interface status check is completed.")
print("\n\n\n")
console.print("Printing the OSPF neighbor status on each device", style= "bold white on magenta")

time.sleep(3)

for items in ospf_n:
    raw = ospf_n[items].strip()
    raw_s = raw.split("\n")
    hdr = Table(show_header = True, header_style="bold black")
    hdr.add_column("Neighbor ID", width = 20)
    hdr.add_column("State", width = 15)
    hdr.add_column("Interface Address", width = 20)
    hdr.add_column("Interface IP", width =20)
    console.print(items, style = "bold black on white")
    for i in range(1,len(raw_s)):
        data = raw_s[i].split()
        nbr_ip = data[0]
        state = data[2]
        addr = data[3]
        name = data[4]
        hdr.add_row(nbr_ip,state,addr,name)
    print(hdr)
    time.sleep(3)

print("OSPF neighbor status check is completed.")
print("\n\n\n")
console.print("Printing the interfaces participating in OSPF", style= "bold white on magenta")


for items in ospf_intf:
    raw = ospf_intf[items].strip()
    raw_s = raw.split("\n")
    hdr = Table(show_header = True, header_style="bold black")
    hdr.add_column("Interface", width = 15)
    hdr.add_column("Area", width = 10)
    hdr.add_column("Intf Address/Mask", width = 20)
    hdr.add_column("OSPF Cost", width =15)
    console.print(items, style = "bold black on white")
    for i in range(1,len(raw_s)):
        data = raw_s[i].split()
        intf = data[0]
        area = data[2]
        netmask = data[3]
        cost = data[4]
        hdr.add_row(intf,area,netmask,cost)
    print(hdr)
    time.sleep(3)