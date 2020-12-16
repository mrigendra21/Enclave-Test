#!/usr/bin/env python3.7

from netmiko import ConnectHandler
import time

#Prepare the list of devices where config needs to be pushed
hosts = open("device-list.txt").read().split("\n")

#Prepare the commands for POD cleanup
cmd = open("pod_cleanup_commands.txt").read().split("\n")

print("Beginning the pod cleanup process in\n")
print("Three \n")
time.sleep(1)
print("Two \n")
time.sleep(1)
print("One \n")
time.sleep(1)

#Loop through each device and send the config set to clean the configs
for H in hosts:
    with ConnectHandler(host=H, port=22, username="admin",password="Cisco123",device_type="cisco_xe") as ch:
        op = ch.send_config_set(cmd)
        print("Config cleanup for {} is completed successfully".format(ch.find_prompt()))


print("All the devices are cleand up")
print("########################")
