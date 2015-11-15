
import re
from collections import OrderedDict

content = None

def go(filename):
    global content
    # with open(filename, mode='rb') as torrent:
    #     print(torrent.read().decode('ISO-8859-1'))
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

def str_bencode(s):
    str_bencoded = "{0}:{1}".format(len(s), s)
    return str_bencoded
# end str_bencode

def int_bencode(i):
    i_bencoded = "i{0}e".format(i)
    return i_bencoded
# end int_bencode

def list_bencode(lst):
    list_bencoded = 'l'
    for item in lst:
        if (type(item) is str):
            s = str_bencode(item)
            list_bencoded += s
        if (type(item) is int):
            s = int_bencode(item)
            list_bencoded += s
        elif (type(item) is list):
            l = list_bencode(item)
            list_bencoded += l
        elif (type(item) is OrderedDict):
            d = dict_bencode(item)
            list_bencoded += d
    # end for
    list_bencoded += 'e'
    return list_bencoded
# end list_bencode

def dict_bencode(dct):
    dct_bencoded = 'd'
    for key, value in dct.items():
        # encode keys
        if (type(key) is str):
            s = str_bencode(key)
            dct_bencoded += s
        elif (type(key) is list):
            l = list_bencode(key)
            dct_bencoded += l
        elif (type(key) is OrderedDict):
            d = dict_bencode(key)
            dct_bencoded += d
        elif (type(key) is int):
            i = int_bencode(key)
            dct_bencoded += i
        # encode values
        if (type(value) is str):
            s = str_bencode(value)
            dct_bencoded += s
        elif (type(value) is list):
            l = list_bencode(value)
            dct_bencoded += l
        elif (type(value) is OrderedDict):
            d = dict_bencode(value)
            dct_bencoded += d
        elif (type(value) is int):
            i = int_bencode(value)
            dct_bencoded += i
    # end for
    dct_bencoded += 'e'
    return dct_bencoded
# end dct_bencode

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
        d = OrderedDict()
        while True:
            key = bdecode(data_list)
            if key == None:
                return d
            value = bdecode(data_list)
            if value == None:
                return d
            d[key] = value
        # end while
    # end elif
# end bdecode
