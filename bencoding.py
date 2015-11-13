
import re

content = None

def go(filename):
    global content
    with open(filename, mode='rb') as torrent:
        list_bytes = list()
        bt = torrent.read(1)
        list_bytes.append(bt)
        while bt:
            bt = torrent.read(1)
            list_bytes.append(bt)
        list_bytes.reverse()
        root_dict = bdecode(list_bytes)
        return root_dict

def bencode(dct):


def bdecode(data_list):
    bt = data_list.pop()
    # print(bt)
    if re.match(r'\d', bt.decode('us-ascii')):
        strlen = bt.decode('us-ascii')
        bt = data_list.pop()
        while re.match(r'\d', bt.decode('us-ascii')):
            strlen += bt.decode('us-ascii')
            bt = data_list.pop()
        string = ''
        for i in range(int(strlen)):
            string += data_list.pop().decode('ISO-8859-1')
            # print(string)
        # print('string', string)
        return string
    elif bt == b'i':
        nombre = ''
        bt = data_list.pop()
        while bt.decode('us-ascii') != 'e':
            nombre += bt.decode('us-ascii')
            bt = data_list.pop()
        # print('nombre', nombre)
        return int(nombre)
    elif bt == b'e':
        return None
    elif bt == b'l':
        l = list()
        while True:
            element = bdecode(data_list)
            if element != None:
                l.append(element)
            else:
                return l
    elif bt == b'd':
        d = dict()
        while True:
            key = bdecode(data_list)
            if key == None:
                return d
            value = bdecode(data_list)
            if value == None:
                return d
            d[key] = value
