import os
import sys
import time
import socket
import select
import logging
import threading

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def makeActive(self,name,conn,fi,juego):    # Obtencion del candado
        self.lock.acquire()
        self.active.append(name)
        logging.debug('Ejecutando')
        conn.sendall(str.encode("play"))
        dato=conn.recv(1024)    # Coordenadas del tiro
        logging.debug(str(dato.decode()))
        juego.jugadorPlay(str(dato.decode()),fi)
        
    def makeInactive(self,name,fi,juego,k):     # Verificacion y liberacion del juego
        self.active.remove(name)
        logging.debug('Liberando candado')
        acabado=juego.verifica(fi,k)
        if not acabado:
            self.libera()
        return acabado,name

    def libera(self):   # Liberacion del candado
        self.lock.release()

class Servidor():
    def __init__(self,host,port,juga):
        self.HOST=host; self.PORT=int(port)
        self.juga=int(juga)
        self.serveraddr=(self.HOST,self.PORT)
        self.listConec=list(); self.listHilos=list()	# Lista de conexiones recibidas e hilos
        self.pool=ActivePool(); self.ganador="" # pool=objeto de los candados
        self.sema=threading.Semaphore(1)    # creacion del semaforo
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.ServerTCP:   # Crea socket TCP
            self.ServerTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.ServerTCP.bind(self.serveraddr)
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
                                                args=(conn,addr,j),)
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

    def iniciarJuego(self,conn,addr,num):
        logging.debug("Recibiendo datos del cliente {}".format(addr))
        try:
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