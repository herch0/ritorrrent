import urllib.request as request
import urllib.parse as parse
import hashlib

import bencoding

# on doit encoder le dictionnaire "info" dans un ordre spécifique
# pour avoir le même hash que celui du tracker
# def infodict_bencode(infodict):
#     keys = ['piece length', 'pieces', 'private', 'name', 'length', 'md5sum', 'files']
#     string = 'd'
#     string += bencoding.str_bencode(keys[0])
#     string += bencoding.int_bencode(infodict[keys[0]])
#     string += bencoding.str_bencode(keys[1])
#     string += bencoding.str_bencode(infodict[keys[1]])
#     if keys[2] in infodict:
#         string += bencoding.str_bencode(keys[2])
#         string += bencoding.int_bencode(infodict[keys[2]])
#     string += bencoding.str_bencode(keys[3])
#     string += bencoding.str_bencode(infodict[keys[3]])
#     # si un seul fichier
#     if keys[4] in infodict:
#         string += bencoding.str_bencode(keys[4])
#         string += bencoding.int_bencode(infodict[keys[4]])
#         string += bencoding.str_bencode(keys[5])
#         string += bencoding.str_bencode(infodict[keys[5]])
#     else:# sinon si plusieurs fichiers
#         string += bencoding.str_bencode(keys[6])
#         string += bencoding.list_bencode(infodict[keys[6]])
#     # end elif
#     string += 'e'
#     return string

port_range = range(6881, 6889)

torrent_dict = bencoding.go('torrent.torrent')

info_dict = torrent_dict['info']

print("============================================")

# print(info_dict)

size = 0
if 'length' in info_dict:
    size = info_dict['length']
else:
    for file in info_dict['files']:
        size += file['length']

infos_bencode = bencoding.dict_bencode(info_dict)
# infos_bencode = "4:info"+infos_bencode+"e"
# print(infos_bencode)

sh1 = hashlib.sha1(infos_bencode.encode('ISO-8859-1'))
# sh1.update(infos_bencode.encode())
info_hash = sh1.digest()

print('hash', info_hash)

# http://open.nyaatorrents.info:6544/announce?info_hash=%e9%5e%c3%a2%055%c0MOp%f3%be3%00%25%89%cc%08%ac7&peer_id=-TR2820-k8geysmrwwsr&port=51413&uploaded=0&downloaded=0&left=0&numwant=80&key=7133af01&compact=1&supportcrypto=1&event=started

tracker_url = torrent_dict['announce']

peer_id = 'RI000112345678900000'

port = port_range[0]

params = {
    'info_hash': info_hash, #urlencoded 20-byte SHA1 hash of the value of the info key from the Metainfo file. Note that the value will be a bencoded dictionary, given the definition of the info key
    'peer_id': peer_id,   #urlencoded 20-byte string used as a unique ID for the client, generated by the client at startup.
    'port': port, #The port number that the client is listening on. Ports reserved for BitTorrent are typically 6881-6889. Clients may choose to give up if it cannot establish a port within this range.
    'uploaded': 0, #The total amount uploaded (bytes) (since the client sent the 'started' event to the tracker) in base ten ASCII.
    'downloaded': 0, #The total amount downloaded (bytes) (since the client sent the 'started' event to the tracker) in base ten ASCII.
    'left': size, # The number of bytes this client still has to download in base ten ASCII. Clarification: The number of bytes needed to download to be 100% complete and get all the included files in the torrent.
    # 'compact': 1, #Setting this to 1 indicates that the client accepts a compact response. The peers list is replaced by a peers string with 6 bytes per peer. The first four bytes are the host (in network byte order), the last two bytes are the port (again in network byte order). It should be noted that some trackers only support compact responses (for saving bandwidth) and either refuse requests without "compact=1" or simply send a compact response unless the request contains "compact=0" (in which case they will refuse the request.)
    # 'no_peer_id': '', #Indicates that the tracker can omit peer id field in peers dictionary. This option is ignored if compact is enabled.
    # started: The first request to the tracker must include the event key with this value.
    # stopped: Must be sent to the tracker if the client is shutting down gracefully.
    # completed: Must be sent to the tracker when the download completes. However, must not be sent if the download was already 100% complete when the client started. Presumably, this is to allow the tracker to increment the "completed downloads" metric based solely on this event.
    'event': 'started',
    # 'ip': '', #Optional. The true IP address of the client machine, in dotted quad format or rfc3513 defined hexed IPv6 address.
    # 'numwant': '', #Optional. Number of peers that the client would like to receive from the tracker. This value is permitted to be zero. If omitted, typically defaults to 50 peers.
    # 'key': '', #Optional. An additional client identification mechanism that is not shared with any peers. It is intended to allow a client to prove their identity should their IP address change.
    # 'trackerid': '' # Optional. If a previous announce contained a tracker id, it should be set here.
}
encoded_params = parse.urlencode(params)

url = tracker_url + "?" + encoded_params

print(url)

with request.urlopen(url) as req:
    print(req.read().decode('ISO-8859-1'))
