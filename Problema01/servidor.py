import os
import sys
import time
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
        self.serveraddr=(self.HOST,self.PORT)
        self.listConec=list(); self.listHilos=[]	# Lista de conexiones recibidas e hilos
        self.NUM_THREADS=5
        self.barrera=threading.Barrier(self.NUM_THREADS)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.ServerTCP:
            self.ServerTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.ServerTCP.bind(self.serveraddr)
            self.ServerTCP.listen(5)
            print("Servidor TCP a la escucha con direccion IP "+str(self.HOST))
            self.servirPorSiempre(self.ServerTCP)

    def servirPorSiempre(self,servidor):
        logging.debug("Esperando instruccion...")
        try:
            i=0
            while i<self.NUM_THREADS:
                conn,addr=servidor.accept()	# Coneccion y direccion del cliente
                print("Conectado a: {}".format(addr))
                self.listConec.append(conn)
                hilo_jugador=threading.Thread(name='Jugador-'+str(i+1),
                                               target=self.iniciarJuego,
                                               args=(self.barrera,conn,addr),)
                self.listHilos.append(hilo_jugador)
                i+=1
            print(self.listHilos)
            logging.debug("Jugadores conectados")
            for t in range(self.NUM_THREADS):
                self.listHilos[t].start()
            while True:
                self.gestion_conexiones()
        except Exception as e:
            print(e)

    def gestion_conexiones(self):
        for conn in self.listConec:
            if conn.fileno()==-1:
                self.listConec.remove(conn)

    def iniciarJuego(self,barr,conn,addr):
        try:
            logging.debug("Recibiendo datos del cliente {} en el {}".format(addr))
            while True:
                data=conn.recv(self.buffer)
                
                if data:
                    logging.debug("Analizando")
                    time.sleep(2)
                
                if not data:
                    print("Conexion cerrada por {}".format(addr))
                    break
        except Exception as e:
            print(e)
        finally:
            conn.close()

s=Servidor()