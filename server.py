# -*- coding: utf-8 -*-
import socket
import struct
import threading
from time import sleep

def send_to_group(message):
	#The 's' means it's a server message, thus it's a hearbeat
	sock.sendto(start_code + 's' + message, (group_multicast, port))

def heartbeat(sock):
	print("Sending heartbeat...")
	message = 'heartbeat'
	while True:
		try:
			#Send Hearbeat to group
			sock.sendto(start_byte + 's' + message, (group_multicast, port))

		except:
			print("ERROR: Could not send heartbeat")
			pass

		sleep(1)


group_multicast = '224.1.1.1'
port = 5007
start_code = '@'

# Create the hearbeat socket
sockhb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockhb.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

#Cria socket for UDP Multicasting
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#Seta TTL das mensagens
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
#Seta timeout para 'listen' não bloquear execução
sock.settimeout(0.2)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((group_multicast, port))
req = struct.pack("4sl", socket.inet_aton(group_multicast), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, req)

#Inicia thread que envia hearbeats a cada 10 segundos
hb = threading.Thread(target=heartbeat, args=(sockhb,))
#Faz thread encerrar execução quando o pai morrer
hb.daemon = True
hb.start()


sleep(5)
print('Ending heartbeat thread')

sock.close()
while True:
	try:
		print sock.recv(10240)
	except:
		pass
