# -*- coding: utf-8 -*-
import socket

group_multicast = '224.1.1.1'
port = 5007
start_byte = "@"

def send_to_group(message):
	sock.sendto(start_byte + 'c' + message, (group_multicast, port))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.sendto("robot", (group_multicast, port))

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
						print("Enviando a seguinte mensagem: " + message)
					except:
						print("Erro ao enviar a mensagem")
				else:
					print("ERRO: Expressão inválida.")
			else:
				print("ERRO: Expressão inválida.")

			