import sys
import getpass
import datetime
import xmlrpc.client

class Cliente():
    def __init__(self,url):
        self.URL=url.lower().split("/")
        self.user=''; self.pasw=''
        self.orden=""; self.instruc=list()
        try:
            self.s=xmlrpc.client.ServerProxy('http://'+self.URL[2])  # Quien atiende las solicitudes
            print("\tSERVICIO RPC")
            s.eleccion(self.URL[3])
            nueva=input('Presione [M] si es que cuenta con un perfil, sino,\nprecione [N] para crear una nueva cuenta: ')
            self.user=input("Usuario: ")
            self.pasw=getpass.getpass("Contraseña: ")

            if nueva.upper()=='M':
                ing=s.ingresar(user,pasw)
            else:
                ing=s.registrar(user,pasw)

            if self.URL=="acceso-remoto":
                self.accRem()
            elif self.URL=="correo":
                self.correo()
            elif self.URL=="archivos":
                self.archivos()
        except Exception as e:
            print(e)
        
    def accRem(self):
        print("Acceso Remoto")

    def correo(self):
        print("Correo")

    def archivos(self):
        print("Archivos")

c=Cliente(sys.argv[1])