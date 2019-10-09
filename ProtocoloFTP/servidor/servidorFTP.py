from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
import os 

def main():
    # Instancia un autorizador dummy para controlar usuarios "virtuales"
    authorizer = DummyAuthorizer()

    # Define un nuevo usuario teniendo todos los permisos y otro para usuarios de solo lectura
    authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())   # Obtener la direcccion del archivo actual

    # Instancia una clase controladora de FTP
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define un string predeterminado para cuando alguien se conecte al cliente
    handler.banner = 'pyftpdlib basado en FTP, listo'

    # Informacion sobre las conexiones y acciones dentro de la carpeta
    # logging.basicConfig(filename='pyftpd.log', level=logging.INFO)
    logging.basicConfig(level=logging.INFO, format='(ServidorTCP) %(message)s',)

    # Instancia una clase servidor FTP y abre conexión en 0.0.0.0:2121
    address = ('127.0.0.1', 2121)   # Direccion IP y puerto del servidor
    server = FTPServer(address, handler)

    # configura un limite de conexiones
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # Inicia el servidor FTP
    server.serve_forever()

if __name__ == '__main__':
    print("Servidor a la escucha")
    main()