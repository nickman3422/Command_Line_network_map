# Created by Nicholas Mangerian 
# must be run using python 3

import os
import ifcfg
import ifaddr


my_ips = []
data = []
adapters = ifaddr.get_adapters()
network_addresses = []
for adapter in adapters:
    for ip in adapter.ips:
        if ":" not in str(ip.ip):
            network_addresses.append([(ip.ip), ip.network_prefix])

for info in network_addresses:
    network = []
    ipAddr = str(info[0])
    my_ips.append(ipAddr)
    ipAddr = (ipAddr[:(ipAddr.rfind("."))] + ".0")
    mask = info[1]
    CIDR = (str(ipAddr) + "/" + str(mask))
    if mask > 16:
        CIDR = (str(ipAddr) + "/" + str(mask))
        response = os.system("nmap " + CIDR + "> myfile.txt")
        f = open("myfile.txt", "r")
        scan = (f.read())
        if "Nmap scan report" in scan:
            scaned_hosts = scan.split("Nmap scan report")
            for scanned_ip in scaned_hosts:
                OS = " "
                if "for" in scanned_ip:
                    ip = scanned_ip.split("\n")[0].split("for ")[1].replace(" ", "")
                    OS = " "
                    if "(" in ip:
                        OS = ip[ip.find("for") + 1:ip.find("(")]
                        ip = ip[ip.find("(") + 1:ip.find(")")]
                    if "PORT " in scanned_ip:
                        services = scanned_ip.split("PORT ")[1]
                        services = services.split("\n")
                        servs = []
                        if "Window" in scanned_ip or "window" in scanned_ip:
                            OS = "Windows"
                        if "Linux" in scanned_ip or "linux" in scanned_ip:
                            OS = "Linux"
                        if "Iphone" in scanned_ip or "iphone" in scanned_ip:
                            OS = "iphone"
                        for service in services:
                            if "/tcp" in service:
                                serv = service.split("/tcp")[1]
                                serv = service.split("/tcp")[1].split(" ")
                                serv = serv[len(serv) - 1].replace(" ", "")
                                servs.append(serv)
                        if OS == " ":
                            network.append([ip, servs])
                        else:
                            network.append([ip, servs, OS])
                            OS = " "

        data.append(network)


def create_box(host):
    box = []
    box.append(("_______________").center(24, '_'))
    box.append(("IP: " + host[0]).center(20, ' '))

    if len(host) > 2:
        box.append(("OS: " + host[2]).center(20, ' '))
    box.append(" ".center(20, ' '))
    box.append(("Services:").center(20, ' '))
    for serv in host[1]:
        box.append((serv).center(20, ' '))

    box.append(("_______________").center(20, '_'))
    return (box)


def print_this_host(subnetbxs):
    print(("|").center(30, ' '))
    print(("|").center(30, ' '))
    print(("|").center(30, ' '))
    print(("|").center(30, ' '))
    print(("|").center(30, ' '))
    for bxs in subnetbxs:
        ip = bxs[1].split(":")[1].replace(" ", "")
        if ip in my_ips:

            for line_num in range(len(bxs)):
                if line_num == 0:
                    print("   ", end='')
                    print(" ", bxs[line_num][4:], end='')
                    print("\t", end='')
                    print("            ")
                    print("    |", end='')
                    print("THIS HOST".center(20, ' '), end='')
                    print("|\t", end='')
                else:
                    print("    |", end='')
                    print(bxs[line_num], end='')
                    print("|\t", end='')
                print("            ")

    return ()


boxes = []
for subnet in range(len(data)):
    Subnetboxes = []
    cur = data[subnet]
    # for top hosts
    for host in range(len(cur)):
        Subnetboxes.append(create_box(data[subnet][host]))
    boxes.append(Subnetboxes)

most_hosts = 0
for subnet in data:
    # print(subnetbxs)
    if len(subnet) > most_hosts:
        most_hosts = len(subnet)

# top:


for subnetbxs in boxes:
    print_this_host(subnetbxs)
    for bx in subnetbxs:
        ip = bx[1].split(":")[1].replace(" ", "")
        if ip in my_ips:
            subnetbxs.remove(bx)
    print(("|").center(30, ' '), end=" ")
    print(" ", end=" ")
    most_lines = 0
    least_lines = 100
    for bx in subnetbxs:
        # print(subnetbxs)
        if len(bx) > most_lines:
            most_lines = len(bx)
    for bx in subnetbxs:
        # print(subnetbxs)
        if len(bx) < most_lines:
            least_lines = len(bx)
    half_way = int(least_lines / 2)

    for line_num in range(most_lines + 1):
        hosts = 1
        for bxs in subnetbxs:
            ip = bxs[0]
            if line_num == 0:
                print(bxs[line_num], end=" ")
                print("\t", end=" ")
            else:
                if len(bxs) > line_num:
                    print("|", end=" ")
                    print(bxs[line_num], end=" ")
                    print("|\t", end=" ")
                else:
                    if line_num == most_lines:

                        if (len(subnetbxs) < most_hosts + 1) and len(subnetbxs) == hosts:
                            
                            print("_".center(11, '_'), end="")
                            print("|", end=" ")
                        else:
                            line = ("|")
                            print(line.center(24, '_'), end=" ")
                            print("______", end=" ")
                    else:
                        line = ("|")
                        print(line.center(24, ' '), end=" ")
                        print("\t", end=" ")
            hosts = hosts + 1

        print("")
        if line_num == most_lines - 1:
            print("              |_________________", end=" ")

        else:
            print(("|").center(30, ' '), end=" ")
            print("\t", end=" ")

    print("")
    print(("|").center(30, ' '), end=" ")
    print("")
