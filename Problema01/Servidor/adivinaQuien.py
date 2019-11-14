'''
    Autores:
        Hernández López Ángel Zait
        Luciano Espina Melisa
'''
import os
import sys
import json
import random as rand

class AdivinaQuien():
    def __init__(self,numJuga):
        self.personaje=""
        self.pistas=list()
        self.numJuga=numJuga
        self.elegirPersonaje()

    def elegirPersonaje(self):
        a=rand.randrange(5)
        if a==0:    self.personaje="Porfirio Diaz"
        elif a==1:  self.personaje="Francisco I Madero"
        elif a==2:  self.personaje="Emiliano Zapata"
        elif a==3:  self.personaje="Venustiano Carranza"
        elif a==4:  self.personaje="Francisco Villa"

    def pistaPersonaje(self,line):
        f=open(self.personaje,'rb')
        i=1; psta=""
        for linea in f.readlines():
            if i==line:
                psta=linea
                break
            i+=1
        return psta