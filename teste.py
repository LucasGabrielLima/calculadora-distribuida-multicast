import socket
import pickle

group_multicast = '224.1.1.1'
port = 5007

class Message(object):
    sender = ''
    sid = None #Server ID
    payload = ''

    def __init__(self, sender = 's', sid = None, payload = ''):
    	self.sender = sender
        self.sid = sid
        self.payload = payload

def send_to_group(message):
	sock.sendto(start_byte+ 'c' + message, (group_multicast, port))
	
message = Message('s', 1, '')
message = pickle.dumps(message)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.sendto(message, (group_multicast, port))
