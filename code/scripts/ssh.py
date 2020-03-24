
import paramiko

# Fonction utilisé pour supprimer les dossier des utilisateurs sur les serveur de vms
# Prend en parametre la liste des  serveurs, la localisation des dossier dans les serveurs,
#  la liste des uids à supprimer, la localisation de la clef ssh 
def ssh_suppr_folder(hosts,location,uids,location_clef):
    # Pour tout les serveur ont essaye de se connecter et ont lance en shell la suppression de tout les dossier voulu,
    # sans se preocuper de leur existance préalable.
    for serveur in hosts:
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.connect(serveur, username=login, password=pwd)
            key_filename=location_clef
            # print("cd "+location+";rm -rf "+" ".join(uids))
            stdin, stdout, stderr = ssh.exec_command("cd "+location+";rm -rf "+" ".join(uids))
            ssh.close()
        except:
            pass
# ssh_suppr_folder(["127.0.0.1"],"londechm","","/home,["eee","dddd","aaa"])