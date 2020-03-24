from ipaddress import IPv4Address,summarize_address_range
import string
import encodings
import re

# Fonction qui prend plusieur plage d'adresse ip, et la liste des adresse deja utilisé/
def attribution_IP(plage_IP,reserved):
    plages=plage_IP.split(",")
    ip=0
    # Pour toute les plages d'@
    for plage in plages:
        # Ont transforme les borne de celles-ci pour pouvoir les comparé
        plage_IP_debut,plage_IP_fin=plage.split("-")
        debutIP = IPv4Address(plage_IP_debut)
        finIP = IPv4Address(plage_IP_fin)
        debut=int(debutIP)
        fin=int(finIP)
    
        reserve=[]
        for ipr in reserved:    
            reserve.append(int(IPv4Address(ipr)))
        nb=debut
        
        # On prend la premiere @Ip non utilisé dans l'une des plage 
        while (nb<=fin) and (ip==0):
            if nb not in reserve:
                ip = nb
            nb+=1

    return str(IPv4Address(ip))

# Fonction qui convertit une addresse mac sous forme AA:BB:CC:DD:EE:FF en forme decimale
def code_hex(mac_string):
    h="0x"+mac_string.replace(":","")
    i=int(h, base=16)
    return i

# Fonction qui convertit une addresse mac sous forme decimal à la form AA:BB:CC:DD:EE:FF
def decode_hex(mac_int):
    mac=hex(mac_int)
    mac="0" + mac[2:]
    mac=':'.join(s for s in re.split(r"(\w{2})", mac.upper()) if s.isalnum())
    return mac

# Fonction prend la liste des mac utilisé par le serveur et la plage d'@ authorisé
def attribution_MAC(min_MAC,max_MAC,reserved):
    # On convertit les adresse en entier pour plus de facilité
    min=code_hex(min_MAC)
    max=code_hex(max_MAC)
    reserved=[ code_hex(x) for x in reserved ]
    iter=min
    mac=0
    # On parcour la liste dans les limite et on prend le premier non utilisé
    while (iter <= max) and (mac==0):
        if iter not in reserved:
            mac=iter
        iter+=1
    mac=decode_hex(mac)
    return mac
    
# Fonction prend la liste des port rdp utilisé par le serveur et la plage de port rdp authorisé
def attribution_RDP(liste_rdp,min_RDP,max_RDP):
    nb=min_RDP
    rdp=0
    # On parcour la liste dans les limite et on prend le premier non utilisé
    while (nb<=max_RDP) and (rdp==0):
        if nb not in liste_rdp:
            rdp = nb
        n=int(nb)
        n+=1
        nb=str(n)
    return rdp

# Fonction mère qui lance juste les autres fonctions et rend le résultat sous forme de tableau
def attribution_vm(plage_IP,ip_used,liste_rdp,min_rdp,max_rdp,min_MAC,max_MAC,mac_used):
    ip=attribution_IP(plage_IP, ip_used)
    rdp = attribution_RDP(liste_rdp,min_rdp,max_rdp)
    mac=attribution_MAC(min_MAC,max_MAC,mac_used)
    return [ip,mac,rdp]


plage_ip = '192.168.176.0-192.168.176.3,192.168.176.7-192.168.176.8'
# plage_id_fin='10.220.1.2'

# plage_id_debut2 = '10.220.2.0'
# plage_id_fin2='10.220.2.2'

# reserved = ['192.168.176.7', '192.168.176.2', '192.168.176.3', '192.168.176.0','192.168.176.1','192.168.176.8']
# ip=attribution_IP(plage_ip,reserved)
# print(ip)

# min_rdp='3388'
# max_rdp='3395'
# liste_rdp=['3388','3390','3391']
# rdp=attribution_RDP(liste_rdp,min_rdp,max_rdp)
# print(rdp)

# mac_used=["08:00:27:00:00:00","08:00:27:00:00:03","08:00:27:00:00:02","08:00:27:00:00:04"]
# mac=attribution_MAC("08:00:27:00:00:00","08:00:27:FF:FF:FF",mac_used)
# print(mac)
