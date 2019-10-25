'''
    Autores:
        Hernández López Ángel Zait
        Luciano Espina Melisa
'''
import os
import sys
import time
import socket

class Cliente():
    def __init__(self,host,port):
        self.HOST=host; self.PORT=int(port)
        self.dirArch=""
        
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as self.ClientTCP:
            self.ClientTCP.connect((self.HOST,self.PORT))
            print("Conectado, esperando a todo los jugadores...\n")
            msgServer=self.ClientTCP.recvfrom(1024)    # Mensaje recibido del servidor
            msgRecib=msgServer[0].decode()   # Mensaje decodificado
            if msgRecib=="go":
                self.aJugar()
            else:
                time.sleep(1)
                print(msgRecib)
    
    def aJugar(self):
        while True:
            msgServer=self.ClientTCP.recvfrom(1024)    # Mensaje recibido del servidor
            msgRecib=msgServer[0].decode()   # Mensaje decodificado
            if msgRecib=='play':
                self.dirArch=input("Ingrese direccion o nombre del achivo")
                with open(self.dirArch, "rb") as archivo:
                    content = archivo.read()
                self.ClientTCP.sendto(content,(self.HOST,self.PORT))  # Envia marca
            else:
                print(msgRecib)


c=Cliente(sys.argv[1],sys.argv[2])