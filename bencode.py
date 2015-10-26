import re

LIST_START = 'list_start'
LIST_END = 'list_end'
STR_START = 'str_start'
STR_END = 'str_end'
INT_START = 'int_start'
INT_END = 'int_end'
DICT_START = 'dict_start'
DICT_END = 'dict_end'
KEY_START = 'key_start'
KEY_END = 'key_end'
VAL_START = 'val_start'
VAL_END = 'val_end'

DICT = 'dict'
INT = 'int'
STR = 'str'
LIST = 'list'
NONE = None

# reg_dict = re.compile(r'd(.*?)e')
# reg_list = re.compile(r'l(.*?)e')
# reg_string = re.compile(r'(\d+):(.*?){\1}')
# reg_integer = re.compile(r'i(\d+)e')

root = None
elements_stack = list()
events_stack = list()
current_state = NONE

def decode(filename):
    elements = list()
    element = list()
    #vérifier si fichier torrent valide
    with open(filename, mode='rb') as torrent:
        bt = torrent.read(1)
        while bt:
            global root, elements_stack, events_stack, current_state
            if re.match(r'\d', bt.decode('ISO-8859-1')):#bt.decode('ISO-8859-1')
                print(current_state)
                length = bt.decode('ISO-8859-1')
                if current_state == DICT_START:
                    current_state = KEY_START
                elif current_state == KEY_START:
                    current_state = VAL_START
                else:
                    current_state = STR_START
                events_stack.append(current_state)
                bt = torrent.read(1)
                while (bt.decode('ISO-8859-1') != ':'):
                    length += bt.decode('ISO-8859-1')
                    bt = torrent.read(1)
                str_bytes = torrent.read(int(length))
                if current_state == KEY_START:
                    print('key', str_bytes.decode('UTF-8'))
                elif current_state == VAL_START:
                    print('value', str_bytes.decode('UTF-8'))
                else:
                    print('string', str_bytes.decode('UTF-8'))
                elements_stack.append(str_bytes.decode('UTF-8'))

            elif bt == b'i':
                elements_stack.append(int())
                events_stack.append(INT_START)
                current_state = INT_START
            elif bt == b'l':
                elements_stack.append(list())
                events_stack.append(LIST_START)
                current_state = LIST_START
            elif bt == b'd':
                elements_stack.append(dict())
                events_stack.append(DICT_START)
                current_state = DICT_START
            elif bt == b'e':
                pass
                # last_event = events_stack.pop()
            bt = torrent.read(1)
