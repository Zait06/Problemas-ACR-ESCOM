'''
    Autores:
        Hernández López Ángel Zait
        Luciano Espina Melisa
'''
import os
import sys
import json
import random as rand
import speech_recognition as sr

class AdivinaQuien():
    def __init__(self,numJuga):
        self.persDoc=""
        self.personaje=list()
        self.pistas=list()
        self.numJuga=numJuga
        self.elegirPersonaje()

    def elegirPersonaje(self):
        a=rand.randrange(5)
        if a==0:    
            self.persDoc="Porfirio Diaz"
            self.personaje=["porfirio diaz"]
        elif a==1:
            self.persDoc="Francisco I Madero"
            self.personaje=["francisco i madero","francisco imadero"]
        elif a==2:
            self.persDoc="Emiliano Zapata"
            self.personaje=["emiliano zapata"]
        elif a==3:
            self.persDoc="Venustiano Carranza"
            self.personaje=["venustiano carranza"]
        elif a==4:
            self.persDoc="Francisco Villa"
            self.personaje=["francisco villa","pancho villa"]

    def convAudText(self,listPosiPersonaje):
        r = sr.Recognizer()
        respuesta = sr.AudioFile('respuesta.wav')
        with respuesta as source:
            audio=r.record(source)
        texto=r.recognize_google(audio,language='es-mx',show_all=True)
        listaTexto=texto['alternative']
        listaRespuestas=list()
        for i in listaTexto:
            listaRespuestas.append(i['transcript'])
        print(listaRespuestas)

    def pistaPersonaje(self,line):
        f=open(self.persDoc,'rb')
        i=1; psta=""
        for linea in f.readlines():
            if i==line:
                psta=linea
                break
            i+=1
        return psta