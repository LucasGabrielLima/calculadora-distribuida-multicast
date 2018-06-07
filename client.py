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

	data = pickle.loads(data)

	try:
		if (data.payload):
			print("Resposta recebida do servidor " + address + ": " + data.payload)

	except:
		print("Você recebeu dados de fontes desconhecidas na porta de recebimento. Por favor mude a porta e tente novamente.")
		sys.exit()


group_multicast = '224.1.1.1'
port = 5010

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
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
					try:
						send_to_group(message)
						receive()
					except:
						print("Erro ao enviar a mensagem")

				else:
					print("ERRO: Expressão inválida.")
			else:
				print("ERRO: Expressão inválida.")
