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