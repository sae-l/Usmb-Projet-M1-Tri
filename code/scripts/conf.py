import configparser
import hashlib
import uuid
# Classe utiliser pour la communication avec le fichier de configuration de l'appli
class Conf:
    __p = ""
    __config = None
    __errorBool = False

    def __init__(self, p):
        self.__p = p
        self.__config = configparser.ConfigParser()
        try:
            self.__config.read(self.__p)
        except:
            print("Erreur lors de la lecture du fichier")
            self.__errorBool = True

    def testError(self):
        return self.__errorBool

    def __build(self):
        with open(self.__p, 'w') as configfile:
            self.__config.write(configfile)

    def readAll(self):
        tab = []
        all = self.__config.items()
        for sec in all:
            section = sec[0]
            content = self.__config.items(section)
            tab.append([section, content])
            # print([section, content])
        return tab
    
    def readSection(self, section):
        tab = []
        section = section.upper()
        content = self.__config.items(section)
        for c in content:
            # print(c)
            tab.append(c)
        return tab
        

    def readOption(self, section, option):
        section = section.upper()
        value = self.__config.get(section, option)
        # print(value)
        return value

    def addSection(self, section):
        section = section.upper()
        self.__config[section] = {}
        self.__build()
    
    def deleteSection(self, section):
        section = section.upper()
        self.__config.remove_section(section)
        self.__build()

    def addOption(self, section, option, value):
        section = section.upper()
        self.__config[section][option] = value
        self.__build()

    def addOptionHash(self, section, option, value):
        salt = uuid.uuid4().hex
        hash_object = hashlib.sha256(salt.encode() + value.encode()).hexdigest() + ':' + salt
        section = section.upper()
        self.__config[section][option] = hash_object
        self.__build()

    def deleteOption(self, section, option):
        section = section.upper()
        self.__config.remove_option(section, option)
        self.__build()

    def resetSection(self, section):
         section = section.upper()
         self.addSection('LDAP')
         self.__build()

    def reset(self):
        self.__config = configparser.ConfigParser()

        self.addSection('LDAP')
        self.addOption('LDAP', 'Serveur_LDAP', 'ldap-bourget.univ-smb.fr')
        self.addOption('LDAP', 'Utilisateur_LDAP', 'default')

        self.addSection('IP')
        self.addOption('IP', 'Adresse_ip_debut', '192.168.0.0')
        self.addOption('IP', 'Adresse_ip_fin', '192.168.255.255')
        self.addOption('IP', 'masque', '0')

        self.addSection('MAC')
        self.addOption('MAC', 'Adresse_mac_debut', '08:00:27:00:00:00')
        self.addOption('MAC', 'Adresse_mac_fin', '08:00:27:FF:FF:FF')

        self.addSection('RDP')
        self.addOption('RDP', 'Port_rdp_debut', '3389')
        self.addOption('RDP', 'Port_rdp_fin', '3391')

        self.__build()