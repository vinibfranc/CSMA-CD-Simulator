# coding: utf-8
import numpy as np

'''Medium is a shared structure accessed by the transmitters, which send data between them'''
class Medium:

    def __init__(self, time_slot):
        self.time_slot = time_slot

        self.clock = 0
        self.medium_size = 8
        self.first_medium = np.zeros(self.medium_size)
        self.last_medium = np.zeros(self.medium_size)
        self.count_writes = 0
        self.last_writes = 0

    def modify_medium(self, val):
        self.last_medium = val
        self.count_writes += 1
        # print("Meio modificado no clock: ", str(self.clock), "contador: ", str(self.count_writes))
        print("Meio modificado no clock: {}, contador {}".format(self.clock, self.count_writes))

    def pass_values(self):
        self.first_medium = self.last_medium
        self.last_medium = np.zeros(self.medium_size)
        self.last_writes = self.count_writes
        self.count_writes = 0
        self.clock += 1

    # Collision detection
    def collision(self):
        # print("Contador de colisoes: ", str(self.count_writes))
        print("Contador de colisoes: {}".format(self.count_writes))
        if self.last_writes > 1:
            return True
        else:
            return False

    # for each cycle detect if a collision occured
    def advance_clock(self):
        # print("Clock avancou e escreveu: ", str(self.count_writes))
        print("Clock avancou e escreveu: {}".format(self.count_writes))
        self.pass_values()

    # Notify the station if is idle or busy
    def sense(self):
        # returns true if channel is busy
        if self.last_writes != 0:
            return True
        else:
            return False
