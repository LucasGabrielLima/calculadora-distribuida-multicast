# -*- coding: utf-8 -*-
import socket
import pickle
import struct

class Message(object):
	sender = ''
	sid = None #Server ID
	payload = ''

	def __init__(self, sender = 'c', sid = None, payload = ''):
		self.sender = sender
		self.sid = sid
		self.payload = payload



def send_to_group(message):
	payload = Message('c', None, message)
	payload = pickle.dumps(payload)
	try:
		sock.sendto(payload, (group_multicast, port))
		print("Enviando a seguinte mensagem: " + message)
	except:
		print("ERRO: Não foi possível enviar a opoeração. Tente novamente")

def receive():
	try:
		data, address = sock.recvfrom(10240)
	except:
		print('Ocorreu um timeout na resposta. Tente novamente.')
		return

	print("Resposta recebida do servidor " + str(address[0]) + ": " + data)


group_multicast = '224.1.1.1'
port = 5010
my_ip = socket.gethostbyname(socket.gethostname())

print("=============================================================================")
print("Implementação de calculadora distribuida usando multicast")
print("Alunos: Adolfo Tognetti Melo Lima Araújo e Lucas Gabriel Lima")
print("Inicio da execução do cliente de IP: " + my_ip)
print("=============================================================================")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind((my_ip, port))
ttl = struct.pack('b', 2)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

message = ""
print("")
print("**Client da calculadora**")
print("**Calcula expressões básicas (+, -, *, /) entre dois números**")
print("")
while (message != "sair"):
	message = raw_input("Digite sua expressão matemática, ou 'sair' caso queira encerrar: ")
	if (message != "sair"):
		if(message == ""):
			print("ERRO: Mensagem não pode ser vazia.")
		else:
			digitos = message.split( )
			if (digitos[0].isdigit() and digitos[2].isdigit()):
				if (digitos[1] == "+" or digitos[1] == "-" or digitos[1] == "*" or digitos[1] == "/"):
					send_to_group(message)
					receive()

				else:
					print("ERRO: Expressão inválida.")
			else:
				print("ERRO: Expressão inválida.")
