# -*- coding: utf-8 -*-
import socket
import struct
import threading
import datetime
import pickle #Biblioteca para serializar objetos de forma que possam ser enviados pela rede
from time import sleep
from collections import OrderedDict

class Message(object):
    sender = ''
    sid = None #Server ID
    payload = ''

    def __init__(self, sender = 's', sid = None, payload = ''):
    	self.sender = sender
        self.sid = sid
        self.payload = payload


def heartbeat(sock, sid):
	print("Sending heartbeat...")
	message = Message('s', sid, 'heartbeat')
	#Serializa objeto da mensagem
	message = pickle.dumps(message)
	while True:
		try:
			#Send Hearbeat to group
			sock.sendto(message, (group_multicast, port))

		except:
			print("ERROR: Could not send heartbeat")
			pass

		sleep(3)

def get_server_id():
	start_time = datetime.datetime.now()
	greater_id = 0

	#Escuta pelo tempo do heartbeat e define o ID igual ao maior ID escutado + 1
	while(datetime.datetime.now() - start_time < datetime.timedelta(seconds = 4)):
		try:
			message, addr = sock.recvfrom(10240)
			message = pickle.loads(message)

			#Adiciona servidores de heartbeats recebidos à lista
			if(message.sender = 's'):
				server_list[str(addr)] = [message.sid, datetime.datetime.now()]
			if(message.sender == 's' and message.sid > greater_id):
				greater_id = message.sid

		except:
			pass

	#Se adiciona na lista de servidores
	my_id = greater_id + 1
	server_list[socket.gethostbyname(socket.gethostname())] = [my_id, datetime.datetime.now()]
	print("Joining server group. My ID is: " + my_id)
	return my_id

#Chamada quando um heartbeat é recebido
def update_server_list(addr):
	now = datetime.datetime.now()
	server_list[addr] = [server_list[addr][0], now]
	print(now ': Receveived heartbeat from ' addr)

#Limpa servidores inativos da lista de servidores
def clean_server_list():
	for server in server_list:
		if (datetime.datetime.now() - server_list[server][1] > datetime.timedelta(seconds = 10):
			server_list.pop(server, None)
			print('Server ' + server + ' has become inactive')


group_multicast = '224.1.1.1'
port = 5007

# Cria o socket para envio de heartbeats
sockhb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 2)
sockhb.settimeout(0.2)
sockhb.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

#Cria socket UDP para comunicação
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

#Seta timeout para 'listen' não bloquear execução
sock.settimeout(0.2)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((group_multicast, port))
req = struct.pack("4sl", socket.inet_aton(group_multicast), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, req)

#Inicia lista (dicionário) de servidores
server_list = {}

#Seta o ID do servidor, de forma incremental em relação aos outros servidores ativos
sid = get_server_id()

#Inicia thread que envia hearbeats a cada 10 segundos
hb = threading.Thread(target=heartbeat, args=(sockhb, sid,))
hb.daemon = True
hb.start()


sleep(5)
print('Ending heartbeat thread')

sock.close()
#while True:
#  print sock.recv(10240)
