# coding: utf-8
import numpy as np
from Frame import Frame
import random
import time

'''Transmitter info and methods to perform CSMA/CD control'''
class Transmitter:

    #Transmitter constructor
    def __init__(self, id, medium_ref):

        self.id = id
        self.medium_ref = medium_ref
        self.frame = None
        self.status = "Pronto"
        self.frame_count = 1

    # Send frame to the Medium
    def send(self, message):
        self.message = message
        print( "Enviando mensagem: " + message.message + " -- " + str(self.id))
        print("Enviando no ciclo: ", self.medium_ref.clock)
        self.send_all(message)
        print("Mensagem enviada!!")

    # Inject characters in the medium if the send is permitted or call collision treatment
    def send_all(self, frame):
        if self.can_send():
            col = False
            for c in frame.message:
                if not col:
                    print("Transmissor ", str(self.id), "vai enviar: ", c)
                    self.medium_ref.modify_medium(c)
                    col = self.medium_ref.collision()
                    time.sleep(1)
                    print("Colisao: ", str(col))
                else:
                    print("JAM detectado no transmissor --> " + str(self.id))
                    self.send_jam()
                    bf = self.calculate_backoff(frame.collision_count)
                    print("Vai esperar por " + str(bf) + "ciclos")
                    time.sleep(bf*0.5)
                    frame.collision_count += 1
                    self.retry(frame)
                    break
        else:
            print(self.id, " nao pode enviar!")
            # channel busy, wait and send again
            time.sleep(0.5)
            self.send_all(frame)

    # Verify if the frame tried to send more than 16 times and abort it
    def retry(self, frame):
        if frame.collision_count > 16:
            print("16 colisoes, abortar transmissao!")
        else:
            self.send_all(frame)

    # Calculate backoff and asign to a poisson distribution based on number of attempts
    def calculate_backoff(self, attempt):
        max_backoff = (2 ** attempt) - 1
        return np.random.poisson(max_backoff)

    # Notify the other transmitters that a collision had occured
    def send_jam(self):
        # print("Ola! Eu sou um sinal de JAM e vim avisar vocês que ocorreu uma colisao no canal!")
        jam_message = "COLISION"
        for c in jam_message:
            self.medium_ref.modify_medium(c)
            print("Enviou: ", c, " de JAM. Transmissor : ", str(self.id))
            time.sleep(0.5)
        print("JAM enviado!")

    # Verify if the actual transmitter can send its frames, i. e., medium idle
    def can_send(self):
        time.sleep(0.1)
        v = self.medium_ref.sense()
        print("Transmissor ", str(self.id), " sensoriou o meio... Pode enviar?: ", str(not v))
        return not v