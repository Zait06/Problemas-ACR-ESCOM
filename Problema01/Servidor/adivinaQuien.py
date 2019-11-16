'''
    Autores:
        Hernández López Ángel Zait
        Luciano Espina Melisa
'''
import os
import sys
import wave
import pyaudio
import random as rand
import speech_recognition as sr

class AdivinaQuien():
    def __init__(self,numJuga):
        self.persDoc=""
        self.personaje=list()
        self.pistas=list()
        self.numJuga=numJuga
        self.r=sr.Recognizer()
        self.elegirPersonaje()

    def elegirPersonaje(self):
        a=rand.randrange(5)
        if a==0:    
            self.persDoc="Porfirio Diaz.txt"
            self.personaje=["porfirio diaz"]
        elif a==1:
            self.persDoc="Francisco I Madero.txt"
            self.personaje=["francisco i madero","francisco imadero"]
        elif a==2:
            self.persDoc="Emiliano Zapata.txt"
            self.personaje=["emiliano zapata"]
        elif a==3:
            self.persDoc="Venustiano Carranza.txt"
            self.personaje=["venustiano carranza"]
        elif a==4:
            self.persDoc="Francisco Villa.txt"
            self.personaje=["francisco villa","pancho villa"]

    def convAudText(self):
        respuesta = sr.AudioFile('respuesta.wav')
        with respuesta as source:
            audio=self.r.record(source)
        print(type(audio))
        texto=self.r.recognize_google(audio,language='es-mx',show_all=True)
        listaTexto=texto['alternative']
        listaRespuestas=list()
        for i in listaTexto:
            listaRespuestas.append(i['transcript'])
        print(listaRespuestas)
        return listaRespuestas

    def pistaPersonaje(self,line):
        f=open(self.persDoc,'rb')
        i=1; psta=""
        for linea in f.readlines():
            if i==line:
                psta=linea
                break
            i+=1
        return psta

    def verifica(self,listaPersona):
        ganador=False
        for pp in listaPersona:
            if pp==self.personaje[0]:
                ganador=True
                break
            if len(self.personaje>1):
                if pp==self.personaje[1]:
                    ganador=True
                    break
        return ganador