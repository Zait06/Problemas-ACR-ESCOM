import sys
import getpass
import datetime
import xmlrpc.client

class Cliente():
    def __init__(self,host,port):
        self.ADDR=host+':'+port
        self.s=xmlrpc.client.ServerProxy('http://'+addr)  # Quien atiende las solicitudes
        self.orden=""; self.instruc=list()
        print("\tSERVICIO RPC")

c=Cliente(sys.argv[1],sys.argv[2])