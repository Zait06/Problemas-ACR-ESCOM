import os

class Archivos():
    def __init__(self):
        self.dir="servicios\\archivos"

    def crearArchivo(self,arch,usua):               # create
        f=open(self.dir+"\\"+usua+"\\"+arch,"w")              # Abre y cierra un archivo
        f.close()
        return self.verContenido(self.dir+"\\"+usua)

    def verContenido(self,usua):                    # readdir
        return str(os.listdir(self.dir+"\\"+usua))

    def ayudameArch(self):                              # help or ?
        coma={
            "create":"Crea un archivo",
            "readdir":"Vista de todos los archivos"
        }
        texto=""
        for c in coma:
            texto+=("\t"+c+"\t"+coma[c]+"\n")
        return texto