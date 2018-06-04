# coding: utf-8
import numpy as np

class Medium:

    def __init__(self, time_slot):
        self.time_slot = time_slot

        # Create a shared list of bits that will be the simulation of the shared media (channel)
        self.medium_size = 8
        self.first_medium = np.zeros(self.medium_size)
        self.last_medium = np.zeros(self.medium_size)
        # np.random.shuffle(self.medium)
        # print("Meio antes do início: {}".format(self.medium))

    def modify_medium(self, frame):
        # arr = Array('i', self.medium)
        # print("Transmissores sensoriando o meio para tentar escrever nele")
        '''for i in range(1, len(self.medium)):
            if i % 2 == 0:
                self.medium[i] = 0
            else:
                self.medium[i] = 1'''
        for i in range(0, frame.size):
            self.last_medium = frame.message[i]
            self.pass_values()
        # print(self.medium)
        # print("Transmissor {} tentando escrever no meio!".format(transmitter_count))

    def pass_values(self):
        self.first_medium = self.last_medium
        self.last_medium = np.zeros(self.medium_size)

