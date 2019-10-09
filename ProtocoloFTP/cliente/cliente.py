from ftplib import FTP
import os
import sys
import time

class Cliente():
    def __init__(self,usu,contra):
        self.HOST="127.0.0.1"
        self.PORT=2121

        ftp = FTP()
        ftp.connect('127.0.0.1', 2121)
        ftp.login(usu, contra, "noaccount")
        try:
            with open('README_COPIA.txt', 'wb') as f:
                ftp.retrbinary('RETR README.txt', f.write)
                f.write(str.encode(time.strftime("%H:%M:%S")))
        except Exception as e:
            print(e)
        finally:
            ftp.quit()

print("Hola\nQuiere ingresar usuario y contrasenia?\n[S]i\t[N]o")
op=input("Opcion: ")
if op=="S":
    name=input("Usuario: ")
    contra=input("Contrasenia: ")
    c=Cliente(name, contra)   
else:
    c=Cliente('anonymous','')
