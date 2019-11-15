'''
    Autores:
        Hernández López Ángel Zait
        Luciano Espina Melisa
'''
import os
import sys
import time
import socket
import select
import logging
import threading
from adivinaQuien import *

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def makeActive(self,name,conn,num):    # Obtencion del candado
        self.lock.acquire()
        self.active.append(name)
        logging.debug('Turno obtenido')
        conn.sendall(str.encode('play'))
        f = open("respuesta.wav", "wb")     # Se crea un archivo de audio donde se guardará el archivo
        while True:
            try:
                dato=conn.recv(1024)
                if dato:                # Si hay datos a recibir, seguir escribiendo
                    f.write(dato)
                else:                   # sino, sal del ciclo
                    break
            except Exception as e:
                print(e)
        logging.debug('Dato recibido y guardado')
        f.close()
        
    def makeInactive(self,name,num):     # Verificacion y liberacion del candado
        self.active.remove(name)
        logging.debug('Liberando candado')
        acabado=False   # juego.verifica(fi,k)  # Verifica si alguien ha adivinado
        if not acabado:
            self.libera()
        return acabado,name

    def libera(self):   # Liberacion del candado
        self.lock.release()

class Servidor():
    def __init__(self,host,port,juga):
        self.HOST=host; self.PORT=int(port)             # IP y Puerto del servidor
        self.juga=int(juga); self.hayGanador=False      # num. jugadores y bandera por si hay un ganador
        self.serveraddr=(self.HOST,self.PORT)           # Dirección del servidor
        self.listConec=list(); self.listHilos=list()	# Lista de conexiones recibidas e hilos
        self.pool=ActivePool(); self.ganador="" # pool=objeto de los candados; ganador=nombre del ganador
        self.sema=threading.Semaphore(1)    # creacion del semaforo con un proceso a la vez
        self.adqu=AdivinaQuien(juga)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.ServerTCP:   # Crea socket TCP
            self.ServerTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)     # No bloqueante
            self.ServerTCP.bind(self.serveraddr)                                    # Servidor a la escucha
            self.ServerTCP.listen(self.juga)
            os.system("cls")
            print("Servidor TCP a la escucha con direccion IP "+str(self.HOST))
            self.servirPorSiempre(self.ServerTCP)

    def servirPorSiempre(self,servidor):
        logging.debug("Esperando a los jugadores...")
        bandera=True
        try:
            j=1
            while True:
                conn,addr=servidor.accept()	# Coneccion y direccion del cliente
                # logging.debug("Conectado a: {}".format(addr))
                self.listConec.append(conn)

                if len(self.listHilos)<self.juga:
                    logging.debug('Conectadndo Jugador-'+str(j)+' con direccion {}'.format(addr))
                    hilo_jugador=threading.Thread(name='Jugador-'+str(j),
                                                target=self.iniciarJuego,
                                                args=(conn,addr,j,self.pool,self.sema),)
                    self.listHilos.append(hilo_jugador)

                if len(self.listHilos)==self.juga and bandera:
                    logging.debug("Creando juego")
                    for t in self.listHilos:
                        t.start()
                        time.sleep(1)
                    bandera=False
                
                if len(self.listConec)>self.juga:
                    conn.sendall(bytes('Jugadores completos','ascii'))
                    self.listConec.remove(conn)
                    conn.close()

                self.gestion_conexiones(self.listConec)
                j+=1

        except Exception as e:
            print(e)

    def gestion_conexiones(self,listaConn):
        for conn in listaConn:
            if conn.fileno()==-1:
                self.listConec.remove(conn)

    def iniciarJuego(self,conn,addr,num,pool,s):
        logging.debug("Listo para jugar")
        try:
            conn.sendall(bytes('go','ascii'))
            conn.sendall(pista)   # Nabdanis la pista a todos los jugadores
            contador=1; numPistas=1
            while not self.hayGanador:  # Si no hay un ganador, seguiremos jugando
                logging.debug("Esperando turno")
                time.sleep(1)
                with s:
                    if not self.hayGanador: # Si no hay un ganador, podemos jugar el turno
                        name=threading.currentThread().getName()    # nombre del jugador actual
                        time.sleep(1)
                        pool.makeActive(name,conn,num)    # Espera de tiro
                        time.sleep(1)
                        pool.makeInactive(name,num)
                    contador+=1
                if numPistas<=5:
                    if contador==self.juga:
                        for i in self.listConec:  # Manda siguiente pista
                            i.sendall(bytes('Se envia la pista siguiente','ascii'))
                            time.sleep(1)
                        contador=0
                elif numPistas>5 and self.hayGanador:
                    for i in self.listConec:
                        i.sendall(bytes('Juego terminado'))
        except Exception as e:
            print(e)
        finally:
            conn.close()

s=Servidor(sys.argv[1],sys.argv[2],sys.argv[3])