'''
    Autores:
        Hernández López Ángel Zait
        Luciano Espina Melisa
'''
import os
import sys
import time
import wave
import socket
import pyaudio

class Cliente():
    def __init__(self,host,port):
        self.HOST=host; self.PORT=int(port)
        self.archivo="personaje.wav"
        
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as self.ClientTCP:
            self.ClientTCP.connect((self.HOST,self.PORT))
            os.system("cls")
            print("Conectado, esperando a todo los jugadores...\n")
            msgServer=self.ClientTCP.recvfrom(1024)    # Mensaje recibido del servidor
            msgRecib=msgServer[0].decode()   # Mensaje decodificado
            if msgRecib=="go":
                self.aJugar()
            else:
                time.sleep(1)
                print(msgRecib)
    
    def aJugar(self):
        print("Preparados para jugar")
        while True:
            msgServer=self.ClientTCP.recvfrom(1024)    # Mensaje recibido del servidor
            msgRecib=msgServer[0].decode()   # Mensaje decodificado
            if msgRecib=='play':
                grab=input("Precione [G] para grabar el audio... ")
                if grab.upper()=='G':
                    self.grabar()
                else:
                    print("Algo anda mal :c")
                with open(self.archivo, "rb") as audio:
                    content = audio.read()
                self.ClientTCP.sendto(content,(self.HOST,self.PORT))  # Envia marca
                print("Enviado...")
            else:
                print(msgRecib)

    def grabar(self):
        # Definicion de parametros
        FORMAT=pyaudio.paInt16
        CHANNELS=2
        RATE=44100
        CHUNK=1024
        duracion=3

        # Inicialización de Pyaudio
        audio=pyaudio.PyAudio()
        stream=audio.open(format=FORMAT,channels=CHANNELS,
                            rate=RATE,input=True,
                            frames_per_buffer=CHUNK)

        print("Grabando...")
        frames=[]

        try:
            # Inicio de grabacion
            for i in range(0,int(RATE/CHUNK*duracion)):
                data=stream.read(CHUNK)
                frames.append(data)
            print("Grabacion terminada")

            # Fin de grabacion
            stream.stop_stream()
            stream.close()
            audio.terminate()

            # Creacion del archivo y guardado del mismo
            waveFile=wave.open(self.archivo,'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
        except Exception as e:
            print(e)

c=Cliente(sys.argv[1],sys.argv[2])