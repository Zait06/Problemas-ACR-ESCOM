import os
import sys
import time
import socket

class Cliente():
    def __init__(self,host,port):
        self.HOST=host; self.PORT=int(port)
        
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as self.ClientTCP:
            self.ClientTCP.connect((self.HOST,self.PORT))
            print("Conectado, esperando a todo los jugadores...")
            msgServer=self.ClientTCP.recvfrom(1024)    # Mensaje recibido del servidor
            msgRecib=msgServer[0].decode()   # Mensaje decodificado
            if msgRecib=="go":
                self.aJugar()
            else:
                print("Algo salio mal")
    
    def aJugar(self):
        while True:
            msgServer=self.ClientTCP.recvfrom(1024)    # Mensaje recibido del servidor
            msgRecib=msgServer[0].decode()   # Mensaje decodificado


c=Cliente(sys.argv[1],sys.argv[2])