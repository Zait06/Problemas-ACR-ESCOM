import os
import sys
import select
import threading
from playsound import playsound		# Librería para reproducir cancion

class Servidor():
	def __init__(self):
		self.HOST="localhost"; self.PORT=8080
		self.NOMBRE_ARCHIVO = "Amiga.mp3"
		self.serveraddr=(self.HOST,self.PORT)

		# Reproduccion de una cancion
		print("Reproducciendo audio...")
		playsound(self.NOMBRE_ARCHIVO)
		print("Fin del audio")
		
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.ServerTCP:
    		self.ServerTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    		self.ServerTCP.bind(self.serveraddr)
    		self.ServerTCP.listen(10)
    		print("Servidor TCP a la escucha con direccion IP "+str(HOST))

s=Servidor()