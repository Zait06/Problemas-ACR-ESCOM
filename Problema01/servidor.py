import os
import sys
import select
import threading
from playsound import playsound		# Librería para reproducir cancion

class Servidor():
	def __init__(self):
		self.HOST="localhost"; self.PORT=8080
		self.buffer=1024	# A cambiar
		self.NOMBRE_ARCHIVO="Amiga.mp3"
		self.serveraddr=(self.HOST,self.PORT)
		self.listConec=list()	# Lista de conexiones recibidas
		
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.ServerTCP:
			self.ServerTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
			self.ServerTCP.bind(self.serveraddr)
			self.ServerTCP.listen(10)
		        print("Servidor TCP a la escucha con direccion IP "+str(self.HOST))
	
			# Reproduccion de un audio
			print("\nReproducciendo audio...")
	    		playsound(self.NOMBRE_ARCHIVO)
	    		print("Fin del audio")
	
	    		# self.servirPorSiempre()

	def servirPorSiempre(self):
	    	try:
    			while True:
	    			conn,addr=self.ServerTCP.accept()	# Conección y direccion del ciente
	    			print("Conectado a: ", addr)
	    			self.listConec.append(conn)
	    			hilo_leer=threading.Tread(target=self.recibir_instruccion,args=[conn,addr])
	    			hilo_leer.start()
	    			self.gestion_conexiones()
	    	except Exception as e:
	    		print(e)
	
	def gestion_conexiones(self):
	    	for conn in self.listConec:
	    		if conn.fileno()==-1:
	    			self.listConec.remove(conn)

	def recibir_instruccion(self,conn,addr):
	    	try:
	    		cur_thread=threading.cur_thread()
	    		print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
	    		while True:
	    			data=conn.recv(self.buffer)
	    			if data:
	    				# Ejecutamos lectura
	    	except Exception as e:
	    		print(e)
	    	finally:
	    		conn.close()

s=Servidor()