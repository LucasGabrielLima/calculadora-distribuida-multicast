import socket

group_multicast = '224.1.1.1'
port = 5007

def send_to_group(message):
	sock.sendto(start_byte+ 'c' + message, (group_multicast, port))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.sendto("robot", (group_multicast, port))