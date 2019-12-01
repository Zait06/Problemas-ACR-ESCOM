import sys
from correo import *
from archivos import *
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class AccesoRemoto():
    def darPaso(self):      # Da el visto bueno para la inspeccion
        return True

class Servidor():
    def __init__(self,HOST,PORT,NAMERPC):
        self.HOST=HOST; self.PORT=int(PORT)
        self.nombre=NAMERPC
        class RequestHandler(SimpleXMLRPCRequestHandler):   # Escucha a todos los solicitantes http
            self.rpc_paths=(self.nombre,)  # Ruta principal

        # Crea el servidor RPC
        with SimpleXMLRPCServer((self.HOST,self.PORT),requestHandler=RequestHandler) as self.server:
            print("Servidor a la escucha")
            self.server.register_introspection_functions()
            self.server.register_function(self.signIn,'ingresar')
            self.server.register_function(self.logIn,'registrar')
            self.server.register_function(self.eleccionCliente,'eleccion')
            self.server.serve_forever()

    def eleccionCliente(self,opc):
        servicio=''
        if opc=="acceso-remoto":
            self.server.register_instance(AccesoRemoto())
            servicio='Acceso Remoto'
        elif opc=="correo":
            self.server.register_instance(Correo())
            servicio='Correo'
        elif opc=="archivos":
            self.server.register_instance(Archivos())
            servicio='Archivos'
        return servicio

    def signIn(self,usua,pasw,direc):                     # Ingresar con un usuario
        perfil=list(); simon=False
        dirAcc="servicios\\"+direc+".txt"
        f=open(dirAcc,"r")               # Abrir archivo de perfiles
        for linea in f.readlines():
            perfil=str(linea).split(':')
            if perfil[0]==usua and perfil[1]==(str(pasw)+"\n"): # Verificación de su existencia
                simon=True
                break
        f.close()                                   # Cierre el archivo
        return simon

    def logIn(self,usua,pasw,direc):                      # Registrar nuevo usuario
        simon=False; otrus=list()
        dirAcc="servicios\\"+direc+".txt"
        try:
            with open(dirAcc,"a") as f:                             # Abrir archivo para agregar un nuevo miembro
                f.write(usua+':'+pasw+'\n')
            otrus=usua.split('@')   # Si es un correo, este solo tomará un string antes del @ para el nombre del usuario
            os.mkdir("servicios\\"+direc+"\\"+otrus[0])                                          # Se crea una carpeta para el nuevo miembro
            with open("servicios\\"+direc+"\\"+otrus[0]+"\\inicio.txt",'w') as f:            # Da archivo de bienvenida
                f.write("Bienvenid@ "+otrus[0]+" al servicio RPC de "+direc)
            simon=True
        except Exception as e:
            print(e)
            simon=False
        return simon


s=Servidor(sys.argv[1],sys.argv[2],sys.argv[3])