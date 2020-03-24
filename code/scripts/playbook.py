import fileinput

# Fonction qui met a jour le playbook, le reecrit entierement a chaque appel,
def createPlaybook(tableau):
    # /On ouvre le fichier en ecriture ou le creer si il n'existe pas
    f = open("static/public/playbook.yml","w+")
    f.write("---")
    # Pour tout les serveur on fait la liste des utilisateur present dessus
    for serveur,nom in tableau:
        # Si le serveur a des utilisateurs
        if nom:
            # On creer la liste de nom formatté comme voulu
            nom = list(dict.fromkeys(nom))
            name = "(|(uid="+nom[0]+")"
            for i in nom[1:]:
                name = name + "(uid="+i+")"
            name = name + ")"
            # On ecrit a la suite la config du serveur
            f.write("\n- hosts: "+serveur+"\n  tasks:\n   - name: Update sssd.conf access filter\n     replace:\n      path: /root/ansibletest\n      after: 'ldap_access_filter = '\n      before: 'debug_level'\n      regexp: '[^\\t\\n].+'\n      replace: '"+name+"'")
    f.close()

# createPlaybook([("maxime",["maxime","addd"]),("local", ["maxime","cons"])])