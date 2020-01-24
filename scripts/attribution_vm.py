from ipaddress import IPv4Address,summarize_address_range
import string
import encodings
import re

def attribution_IP(plage_IP_debut,plage_IP_fin,reserved):
    debutIP = IPv4Address(plage_IP_debut)
    finIP = IPv4Address(plage_IP_fin)
    debut=int(debutIP)
    fin=int(finIP)
    
    reserve=[]
    for ip in reserved:    
        reserve.append(int(IPv4Address(ip)))

    nb=debut
    ip=0
    while (nb<=fin) and (ip==0):
        if nb not in reserve:
            ip = nb
        nb+=1

    return str(IPv4Address(ip))


def code_hex(mac_string):
    h="0x"+mac_string.replace(":","")
    i=int(h, base=16)
    return i

def decode_hex(mac_int):
    mac=hex(mac_int)
    mac="0" + mac[2:]
    mac=':'.join(s for s in re.split(r"(\w{2})", mac.upper()) if s.isalnum())
    return mac

def attribution_MAC(min_MAC,max_MAC,reserved):
    min=code_hex(min_MAC)
    max=code_hex(max_MAC)
    reserved=[ code_hex(x) for x in reserved ]
    iter=min
    mac=0
    while (iter <= max) and (mac==0):
        if iter not in reserved:
            mac=iter
        iter+=1
    mac=decode_hex(mac)
    return mac
    
def attribution_RDP(liste_rdp,min_RDP,max_RDP):
    nb=min_RDP
    rdp=0
    while (nb<=max_RDP) and (rdp==0):
        if nb not in liste_rdp:
            rdp = nb
        n=int(nb)
        n+=1
        nb=str(n)
    return rdp

def attribution_vm(plage_IP_deb,plage_ip_fin,ip_used,liste_rdp,min_rdp,max_rdp,min_MAC,max_MAC,mac_used):
    ip=attribution_IP(plage_IP_deb, plage_ip_fin, ip_used)
    rdp = attribution_RDP(liste_rdp,min_rdp,max_rdp)
    mac=attribution_MAC(min_MAC,max_MAC,mac_used)
    return [ip,mac,rdp]


# plage_id_debut = '10.220.1.0'
# plage_id_fin='10.220.1.2'

# plage_id_debut2 = '10.220.2.0'
# plage_id_fin2='10.220.2.2'

# reserved = ['10.220.1.0', '10.220.1.1', '10.220.1.2', '10.220.2.1']
# ip=attribution_IP(plage_id_debut,plage_id_fin,reserved)
# print(ip)

# min_rdp='3388'
# max_rdp='3395'
# liste_rdp=['3388','3390','3391']
# rdp=attribution_RDP(liste_rdp,min_rdp,max_rdp)
# print(rdp)

# mac_used=["08:00:27:00:00:00","08:00:27:00:00:03","08:00:27:00:00:02","08:00:27:00:00:04"]
# mac=attribution_MAC("08:00:27:00:00:00","08:00:27:FF:FF:FF",mac_used)
# print(mac)
