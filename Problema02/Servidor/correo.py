import os
import zipfile

class Correo():
    def __init__(self):
        self.dir="servicios\\correo"

    def mandarComprimido(self,usua,nomComp,destino):
        direc=self.dir+"\\"+usua
        comp_zip=zipfile.ZipFile(direc+"\\"+nomComp+".zip", 'w') # creacion del archivo comprimido
        # Recorremos todo el directorio carpetas,subcarpetas,archivos
        for folder, subfolders, files in os.walk(direc):
            for file in files:  # Recorrer todos los archivos
                if not str(file)==nomComp+".zip": # Si el archivo no es igual al nombre del archivo zip, comprimirlo
                    comp_zip.write(os.path.join(folder, file), 
                                    os.path.relpath(os.path.join(folder,file),direc),
                                    compress_type = zipfile.ZIP_DEFLATED)
        comp_zip.close()    # Cerramos el archivo comprimido

    def ayudameCorr(self):                              # help or ?
        coma={
            "sendzip":"Mandar un correo con un zip"
        }
        texto=""
        for c in coma:
            texto+=("\t"+c+"\t"+coma[c]+"\n")
        return texto