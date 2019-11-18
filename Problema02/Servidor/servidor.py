import sys
from correo import *
from archivos import *
from accesoRemoto import *
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class Servidor():
    def __init__(self,HOST,PORT,NAME):
        self.HOST=HOST; self.PORT=int(PORT)
        class RequestHandler(SimpleXMLRPCRequestHandler):   # Escucha a todos los solicitantes http
            self.rpc_paths = (NAME,)  # Ruta principal

        # Crea el servidor RPC
        with SimpleXMLRPCServer((self.HOST,self.PORT),requestHandler=RequestHandler) as self.server:
            print("Servidor a la escucha")
            self.server.register_introspection_functions()
            self.server.register_function(self.signIn,'ingresar')
            self.server.register_function(self.logIng,'registrar')
            self.server.register_function(self.eleccionCliente,'eleccion')
            self.server.serve_forever()

    def eleccionCliente(self,opc):
        servicio=''
        if opc==1:
            self.server.register_instance(AccesoRemoto())
            servicio='Acceso Remoto'
        elif opc==2:
            self.server.register_instance(Correo())
            servicio='Correo'
        elif opc==3:
            self.server.register_instance(Archivos())
            servicio='Archivos'
        return servicio

    def signIn(self,usua,pasw):                     # Ingresar con un usuario
        perfil=list(); simon=False
        f=open("../perfiles.txt","r")               # Abrir archivo de perfiles
        for linea in f.readlines():
            perfil=str(linea).split(':')
            if perfil[0]==usua and perfil[1]==(str(pasw)+"\n"): # Verificación de su existencia
                simon=True
                break
        f.close()                                   # Cierre el archivo
        return simon

    def logIn(self,usua,pasw):                      # Registrar nuevo usuario
        simon=False
        try:
            with open("../perfiles.txt","a") as f:  # Abrir archivo para agregar un nuevo miembro
                f.write(usua+':'+pasw+'\n')
            os.mkdir(usua)                          # Se crea una carpeta para el nuevo miembro
            with open("./"+usua+"/inicio.txt",'w') as f:    # Da archivo de bienvenida
                f.write("Bienvenid@ "+usua+" al servicio RPC")
            simon=True
        except Exception as e:
            print(e)
            simon=False
        return simon


s=Servidor(sys.argv[1],sys.argv[2],sys.argv[3])