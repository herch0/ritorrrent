import re

reg_dict = re.compile(r'd(.*?)e')
reg_list = re.compile(r'l(.*?)e')
reg_string = re.compile(r'(\d+):(.*?){\1}')
reg_integer = re.compile(r'i(\d+)e')

current = '_dict'
root = None
current_element = None

def _str(bt, str):
    print('string')

def _int(bt, num):
    print('integer')

def _list(bt, lst):
    print('list')

def _dict(bt, dct):
    print('dict')

def start(bt):
    global current, root, current_element
    print('current', current)
    if re.match(r'\d', bt.decode('ISO-8859-1')):
        current = '_str'
    elif bt == b'i':
        current = '_int'
    elif bt == b'l':
        current = '_list'
    elif bt == b'd':
        current = '_dict'
    func = globals()[current]
    if root == None:
        root = func(bt)
    else:
        current_element = func(bt)


def decode(filename):
    elements = list()
    element = list()
    #vérifier si fichier torrent valide
    with open(filename, mode='rb') as torrent:
        bt = torrent.read(1)
        while bt:
            start(bt)
            if (bt != b'e'):
                element.append(bt)
            else:
                elements.append(element)
                #print(element)
                break
                element = list()
            bt = torrent.read(1)
