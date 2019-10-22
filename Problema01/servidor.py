import os
import sys
import time
import socket
import select
import logging
import threading

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class Servidor():
    def __init__(self,host,port,juga):
        self.HOST=host; self.PORT=int(port)
        self.juga=int(juga)
        self.serveraddr=(self.HOST,self.PORT)
        self.listConec=list(); self.listHilos=list()	# Lista de conexiones recibidas e hilos
        self.barrera=threading.Barrier(self.juga)    # Crear barrera
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.ServerTCP:   # Crea socket TCP
            self.ServerTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.ServerTCP.bind(self.serveraddr)
            self.ServerTCP.listen(self.juga)
            print("Servidor TCP a la escucha con direccion IP "+str(self.HOST))
            self.servirPorSiempre(self.ServerTCP)

    def servirPorSiempre(self,servidor):
        logging.debug("Esperando a los jugadores...")
        try:
            j=0
            while j<self.juga:
                conn,addr=servidor.accept()	# Coneccion y direccion del cliente
                print("Conectado a: {}".format(addr))
                self.listConec.append(conn)
                hilo_jugador=threading.Thread(name='Jugador-'+str(j+1),
                                               target=self.iniciarJuego,
                                               args=(conn,addr),)
                self.listHilos.append(hilo_jugador)
                j+=1

            logging.debug("Creando juego")

            for t in self.listHilos:
                t.start()

            #while True:
                #self.gestion_conexiones()

        except Exception as e:
            print(e)

    def gestion_conexiones(self):
        for conn in self.listConec:
            if conn.fileno()==-1:
                self.listConec.remove(conn)

    def iniciarJuego(self,conn,addr):
        try:
            logging.debug("Recibiendo datos del cliente {} en el {}".format(addr))
            while True:
                data=conn.recv(1024)
                
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

s=Servidor(sys.argv[1],sys.argv[2],sys.argv[3])