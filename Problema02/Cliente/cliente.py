import os
import sys
import getpass
import datetime
import xmlrpc.client

class Cliente():
    def __init__(self,url):
        self.URL=url.lower().split("/")
        self.user=''; self.pasw=''
        self.orden=""; self.instruc=list()
        self.servicio=""
        try:
            os.system("cls")
            self.s=xmlrpc.client.ServerProxy('http://'+self.URL[2])  # Quien atiende las solicitudes
            print("\t\tSERVICIO RPC")
            self.servicio=self.s.eleccion(self.URL[3])
            nueva=input('Presione [M] si es que cuenta con un perfil, sino,\nprecione [N] para crear una nueva cuenta: ')
            self.user=input("Usuario: ")
            self.pasw=getpass.getpass("Contraseña: ")

            if nueva.upper()=='M':
                ing=self.s.ingresar(self.user,self.pasw,self.URL[3])
            else:
                ing=self.s.registrar(self.user,self.pasw,self.URL[3])

            print("\n\tServicio de "+self.servicio+". Sesión iniciada")
            if self.URL[3]=="acceso-remoto":
                self.accRem()
            elif self.URL[3]=="correo":
                self.correo()
            elif self.URL[3]=="archivos":
                self.archivos()
        except Exception as e:
            print(e)
        
    def accRem(self):
        print("jeje")

    def correo(self):
        nuser=self.user.split("@")
        while True:
            orden=input(nuser[0]+">> ")
            instruc=orden.lower().split()
            if instruc[0]=='sendzip':                                # Crear un archivo
                print(self.s.crearArchivo(nuser[0],instruc[1],instruc[2]))
            elif instruc[0]=='help' or instruc[0]=='?':             # Lista de comandos
                print(self.s.ayudameCorr())
            elif instruc[0]=='exit':                                # Salir de todo
                print("\n\t\tHASTA PRONTO "+user+"\n")
                break
            else:
                print("Instruccion incorrecta, intente de nuevo\n")

    def archivos(self):
        while True:
            orden=input("user@"+self.user+">> ")
            instruc=orden.lower().split()
            if instruc[0]=='create':                                # Crear un archivo
                print(self.s.crearArchivo(instruc[1],self.user))
            elif instruc[0]=='readdir':                             # Vista de todos los archivos
                print(self.s.verContenido(self.user))
            elif instruc[0]=='help' or instruc[0]=='?':             # Lista de comandos
                print(self.s.ayudameArch())
            elif instruc[0]=='exit':                                # Salir de todo
                print("\n\t\tHASTA PRONTO "+user+"\n")
                break
            else:
                print("Instruccion incorrecta, intente de nuevo\n")

c=Cliente(sys.argv[1])