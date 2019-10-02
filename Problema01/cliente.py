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
            print("Conectado...")
            time.sleep(10)

c=Cliente()