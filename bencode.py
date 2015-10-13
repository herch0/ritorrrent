import re

reg_dict = re.compile(r'd(.*?)e')
reg_list = re.compile(r'l(.*?)e')
reg_string = re.compile(r'(\d+):(.*?){\1}')
reg_integer = re.compile(r'i(\d+)e')

def decode(filename):
    #vérifier si fichier torrent valide
    #torrent = open(filename, mode='r', encoding='ASCII')
    with open(filename, mode='rb') as torrent:
        bt = torrent.read(1)
        while bt:
            print(bt)
            bt = torrent.read(1)
