import os
import sys
import time
import socket

class Cliente():
    def __init__(self):
        self.HOST="127.0.0.1"
        self.PORT=8080
        
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as self.ClientTCP:
            self.ClientTCP.connect((self.HOST,self.PORT))
            print("Conectado, esperando a todo los jugadores...")
            msgServer=self.ClientTCP.recvfrom(1024)    # Mensaje recibido del servidor
            msgRecib=msgServer[0].decode()   # Mensaje recibido y decodificado

c=Cliente()