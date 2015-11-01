
import re

content = None

def init(filename):
    global content
    with open(filename, mode='rb') as torrent:
        list_bytes = list()
        bt = torrent.read(1)
        list_bytes.append(bt)
        while bt:
            bt = torrent.read(1)
            list_bytes.append(bt)
        list_bytes.reverse()
        root_dict = decode(list_bytes)
        print(root_dict)

def decode(data_list):
    bt = data_list.pop()
    print(bt)
    if re.match(r'\d', bt.decode('us-ascii')):
        strlen = bt.decode('us-ascii')
        bt = data_list.pop()
        while re.match(r'\d', bt.decode('us-ascii')):
            strlen += bt.decode('us-ascii')
            bt = data_list.pop()
        string = ''
        for i in range(int(strlen)):
            string += data_list.pop().decode('us-ascii')
        return string
    elif bt == b'i':
        decode(data_list)
        pass
    elif bt == b'l':
        decode(data_list)
        pass
    elif bt == b'd':
        d = dict()
        key = decode(data_list)
        value = decode(data_list)
        d[key] = value
        return d
