#!/usr/bin/env python3.7

import yaml
import xmltodict
from jinja2 import Template
from ncclient import manager
import getpass


def OSPF(nccon, rpc,H):
#Calling the edit_config function to send the payload
    try:
        rep = nccon.edit_config(rpc, target='running')
        print("Device config for {} host is sent\n".format(H))
        # Process the netconf respone and print the rpc status
        print("Review the RPC Reply received from the device", rep)

    except:
        print("Device config couldn't be done for {} host".format(H))

#Main execution of the code starts from here
if __name__=='__main__':

# Take the user input for Username and Password
    User = input("Please enter the Username >")
    Pass = getpass.getpass("Please enter the Password >")

# Load the network configuration file and store it in cache named "config"
    with open("Device_Configs.yaml") as f:
        config = yaml.safe_load(f.read())

# Load the jinja file and create a template for OSPF related config
    with open("ospf.j2") as f:
        ospf_template = Template(f.read())


#Prepare the devices for Configuration
    for device in config["devices"]:
        print("Creating OSPF specific configuration for {} router".format(device["name"]))
        with open("ospf/{}.cfg".format(device["name"]), "w") as f:
            ospf_config = ospf_template.render(ospf=device["ospf"],networks=device["ospf"]["networks"],interfaces=device["ospf"]["interfaces"])
            f.write(ospf_config)


# Establish a netconf connection with the device
        print("Establishing netconf session with {}".format(device["name"]))
        try:
            with manager.connect(host=device["host_ip"],port=device["netconf_port"],username=User,password=Pass,hostkey_verify=False,device_params={'name':'csr'}) as m_con:
                print("===================================")
                print("Netconf connection to {} is established correctly""".format(device["name"]))
                with open("ospf/{}.cfg".format(device["name"])) as f:
                    rpc = f.read()
                print("Calling the device to process the OSPF config")
                OSPF(m_con,rpc,device["name"])
        except:
            print("There is some problem with establishing the netconf connection")
