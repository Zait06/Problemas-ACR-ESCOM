import os
import sys
import socket
import select
import logging
import threading

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

class Servidor():
    def __init__(self):
        self.HOST="127.0.0.1"; self.PORT=8080
        self.buffer=1024; self.juga=0
        self.NOMBRE_ARCHIVO="Amiga.mp3"
        self.serveraddr=(self.HOST,self.PORT)
        self.listConec=list()	# Lista de conexiones recibidas
        self.audio=open("recibido.mp3","wb")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.ServerTCP:
            self.ServerTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.ServerTCP.bind(self.serveraddr)
            self.ServerTCP.listen(5)
            print("Servidor TCP a la escucha con direccion IP "+str(self.HOST))
            self.servirPorSiempre(self.ServerTCP)

    def servirPorSiempre(self,servidor):
        logging.debug("Esperando instruccion...")
        try:
            while True:
                conn,addr=servidor.accept()	# Coneccion y direccion del ciente
                logging.debug("Conectado a: ", addr)
                self.listConec.append(conn)
                self.juga+=1
                hilo_jugador=threading.Tread(target=self.recibir_instruccion,
                                                args=[conn,addr],
                                                name="Jugador-"+str(self.juga))
                hilo_jugador.start()
                self.gestion_conexiones()
        except Exception as e:
            print(e)

    def gestion_conexiones(self):
        for conn in self.listConec:
            if conn.fileno()==-1:
                self.listConec.remove(conn)

    def recibir_instruccion(self,conn,addr):
        try:
            cur_thread=threading.current_thread()
            logging.debug("Recibiendo datos del cliente {} en el {}".format(addr,cur_thread))
            while True:
                data=conn.recv(self.buffer)
                if data:
                    print("Recibiendo insturccion...")
                    self.audio.write(data)
        except Exception as e:
            print(e)
        finally:
            conn.close()

s=Servidor()