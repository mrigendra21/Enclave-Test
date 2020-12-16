#!/usr/bin/env python3.7
import yaml
import xmltodict
from jinja2 import Template
from ncclient import manager
import getpass



#capability check supported by device
"""
with manager.connect(host="192.168.166.101",port="830",username="admin",password="Cisco123",hostkey_verify=False, device_params={'name':'csr'}) as m:
    capa = m.server_capabilities
    capa_dict = capa._dict
    for items in capa_dict:
        print(items)
"""

def interface(nccon, rpc,H):
#Calling the edit_config function to send the payload
    try:
        rep = nccon.edit_config(rpc, target='running')
        print("Device config for {} host is sent\n\n".format(H))
        # Process the netconf respone and print the rpc status
        print("Review the RPC Reply received from the device\n\n", rep)
    except:
        print("Device config couldn't be done for {} host\n\n".format(H))


#Main execution of the code starts from here
if __name__=='__main__':

# Take the user input for Username and Password
    User = input("Please enter the Username >")
    Pass = getpass.getpass("Please enter the Password >")


# Load the network configuration file and store it in cache named "config"
    with open("Device_Configs.yaml") as f:
        config = yaml.safe_load(f.read())


# Load the jinja file and create a template for Interface related config
    with open("interface.j2") as f:
        interface_template = Template(f.read())
    

#Prepare the devices for Configuration
    for device in config["devices"]:
        print("Creating interface specific configuration for {} router".format(device["name"]))
        with open("interface/{}.cfg".format(device["name"]), "w") as f:
            intf_config = interface_template.render(interfaces=device["interfaces"],loopbacks=device["loopbacks"])
            f.write(intf_config)


# Establish a netconf connection with the device
        print("Establishing netconf session with {}".format(device["name"]))
        try:
            with manager.connect(host=device["host_ip"],port=device["netconf_port"],username=User,password=Pass,hostkey_verify=False,device_params={'name':'csr'}) as m_con:
                print("===================================")
                print("Netconf connection to {} is established correctly""".format(device["name"]))
                with open("interface/{}.cfg".format(device["name"])) as f:
                    rpc = f.read()
                print("Calling the device to process the interface config")
                interface(m_con,rpc,device["name"])
        except:
            print("There is some problem with establishing the netconf connection")
            