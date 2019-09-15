import os
import sys
import select
import threading
from playsound import playsound		# Librería para reproducir cancion

class Servidor():
	def __init__(self):
		self.HOST="localhost"; self.PORT=8080
		self.NOMBRE_ARCHIVO = "Amiga.mp3"
		print("Reproducciendo audio...")
		playsound(self.NOMBRE_ARCHIVO)
		


s=Servidor()