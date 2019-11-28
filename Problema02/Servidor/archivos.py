import os


class Archivos():
    def ayudame(self):                              # help or ?
        coma={
            "null":"Ping al servidor"
        }
        texto=""
        for c in coma:
            texto+=("\t"+c+"\t"+coma[c]+"\n")
        return texto