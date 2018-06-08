# -*- coding: utf-8 -*-
import socket
import struct
import threading
import datetime
import os
import string
import pickle #Biblioteca  utilizada para serializar objetos de forma que possam ser enviados pela rede
from time import sleep

class Message(object):
	sender = ''
	sid = None #Server ID
	payload = ''

	def __init__(self, sender = 's', sid = None, payload = ''):
		self.sender = sender
		self.sid = sid
		self.payload = payload


def heartbeat(sock, sid):
	now = str(datetime.datetime.now().replace(microsecond=0))
	print(now + ': Iniciando thread de heartbeats.')
	message = Message('s', sid, 'heartbeat')
	#Serializa objeto da mensagem
	message = pickle.dumps(message)
	while True:
		try:
			#Envia heartbeat para grupo
			sock.sendto(message, (group_multicast, port))

		except:
			print("ERRO: Não foi possível enviar o heartbeat")
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
			if(message.sender == 's'):
				server_list[str(addr[0])] = [message.sid, datetime.datetime.now()]
			if(message.sender == 's' and message.sid > greater_id):
				greater_id = message.sid

		except:
			pass

	#Se adiciona na lista de servidores
	my_id = greater_id + 1
	server_list[socket.gethostbyname(socket.gethostname())] = [my_id, datetime.datetime.now()]
	now = str(datetime.datetime.now().replace(microsecond=0))
	print(now + ": Entrando no grupo de servidores. Meu ID é: " + str(my_id))
	return my_id

#Chamada quando um heartbeat é recebido
def update_server_list(message, addr):
	now = datetime.datetime.now().replace(microsecond=0)
	server_list[addr] = [message.sid, now]
	if(addr != socket.gethostbyname(socket.gethostname())):
		print(str(now) + ': Hearbeat recebido de ' + str(addr) + '. Atualizando tabela de servidores.')


#Limpa servidores inativos a mais de 10 segundos da lista de servidores
def clean_server_list():
	for server in server_list:
		if (datetime.datetime.now() - server_list[server][1] > datetime.timedelta(seconds = 10)):
			server_list.pop(server, None)
			now = str(datetime.datetime.now().replace(microsecond=0))
			print(now + ': Server ' + str(server) + ' se tornou inativo. Removendo-o da lista.')

def handle_req(req, addr):
	smaller_id = sid
	now = str(datetime.datetime.now().replace(microsecond=0))

	#Busca servidor com menor ID (líder)
	for server in server_list:
		if(server_list[server][0] < smaller_id):
			smaller_id = server_list[server][0]

	if(smaller_id == sid):
		print(now + ": Eu tenho o menor ID, portanto sou o líder!")
		res = threading.Thread(target=response_thread, args=(req, addr,))
		res.daemon = True #Faz thread morrer caso pai encerre
		res.start()
	else:
		print(now + ": Eu não sou o líder. Não responderei a requisição.")


def response_thread(message, addr):
	now = str(datetime.datetime.now().replace(microsecond=0))
	print(now + ": Iniciando thread de resposta.")
	#Parseia operando e operações do payload da mensagem
	parsed = string.split(message.payload, ' ')
	a = int(parsed[0])
	b = int(parsed[2])
	op = parsed[1]

	if(op == '+'):
		response = a + b
	elif(op == '-'):
		response = a - b
	elif(op == '/'):
		if(b != 0):
			response = a / b
		else:
			response = "Não é possível dividir por 0."
	elif(op == '*'):
		response = a * b
	else:
		response = "Não foi possível atender à requisição."
		print("Não foi possível atender à requisição.")

	#Cria socket para responder a requisição do cliente
	response_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	#Envia resposta ao cliente
	response_sock.sendto(str(response), (addr, port))

	now = str(datetime.datetime.now().replace(microsecond=0))
	print(now + ": Enviando resposta para o cliente " + str(addr) + ": " + str(response))

	#Encerra o socket
	response_sock.close()

def receive(data, address):
	message = pickle.loads(data)

	try:
		if(message.sender == 'c'):
			now = str(datetime.datetime.now().replace(microsecond=0))
			print(now + ": Requisição recebida do cliente " + str(address) + ": " + message.payload)
			clean_server_list()
			handle_req(message, address)
		

		if(message.sender == 's' and message.payload == 'heartbeat'):
			update_server_list(message, address)

	except:
		print("O servidor recebeu dados de fontes desconhecidas na porta de recebimento.")



my_ip = socket.gethostbyname(socket.gethostname())

print("=============================================================================")
print("Implementação de calculadora distribuida usando multicast")
print("Alunos: Adolfo Tognetti Melo Lima Araújo e Lucas Gabriel Lima")
print("Inicio da execução do servidor de IP: " + my_ip)
print("=============================================================================")


group_multicast = '224.1.1.1'
port = 5010

# Cria o socket para envio de heartbeats
sockhb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 2)
sockhb.settimeout(0.2)
sockhb.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
now = str(datetime.datetime.now().replace(microsecond=0))
print(now + ": Criado socket para envio de heartbeats.")

#Cria socket UDP para comunicação
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

#Seta timeout para 'listen' não bloquear execução
sock.settimeout(0.2)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((group_multicast, port))
req = struct.pack("4sl", socket.inet_aton(group_multicast), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, req)
now = str(datetime.datetime.now().replace(microsecond=0))
print(now + ": Criado socket para comunicação.")

#Inicia lista (dicionário) de servidores
server_list = {}

#Seta o ID do servidor, de forma incremental em relação aos outros servidores ativos
sid = get_server_id()

#Inicia thread que envia hearbeats a cada 3 segundos
hb = threading.Thread(target=heartbeat, args=(sockhb, sid,))
hb.daemon = True #Faz thread morrer caso pai encerre
hb.start()

print(socket.gethostbyname(socket.gethostname()))
while True:
	try:
		data, address = sock.recvfrom(10240)
		receive(data, address[0])
	except KeyboardInterrupt:
		# Se receber um ctrl + c
		break

	except:
		pass


sock.close()
sockhb.close()
now = str(datetime.datetime.now().replace(microsecond=0))
print(now + ": Encerrando sockets inicializados.")
print(now + ': Encerrando execução do programa principal e da thread de heartbeats.')
