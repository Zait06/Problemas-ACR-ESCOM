from ftplib import FTP
import os
import sys
import time

class Cliente():
    def __init__(self,usu,contra):
        self.HOST="127.0.0.1"
        self.PORT=2121

        ftp = FTP()
        ftp.connect(self.HOST, self.PORT)
        ftp.login(usu, contra, "noaccount")
        try:
            with open('README_COPIA.txt', 'wb') as f:
                ftp.retrbinary('RETR README.txt', f.write)
                f.write(str.encode(time.strftime("%H:%M:%S")))
            a=input("Nombre de la carpeta nueva: ")
            ftp.mkd(a)
        except Exception as e:
            print(e)
        finally:
            print("Tarea finalizada")
            ftp.quit()

print("Hola\nQuiere ingresar usuario y contrasenia?\n[S]i\t[N]o")
op=input("Opcion: ")
if op=="S" or op=='s':
    name=input("Usuario: ")
    contra=input("Contrasenia: ")
    c=Cliente(name, contra)   
else:
    c=Cliente('anonymous','')
