# coding: utf-8
import numpy as np

'''Simulate the channel (medium) of transmission of frames'''
class Medium:

    def __init__(self, time_slot):
        self.time_slot = time_slot

        self.medium_size = 8
        self.first_medium = np.zeros(self.medium_size)
        self.last_medium = np.zeros(self.medium_size)
        self.count_writes = 0

    # Medium is modified by transmition or JAM signal
    def modify_medium(self, val):
        self.last_medium = val
        self.count_writes += 1

    # List which contains the values in media por each cycle
    def pass_values(self):
        self.first_medium = self.last_medium
        self.last_medium = np.zeros(self.medium_size)
        self.count_writes = 0

    # A collision occurs if there are more than 1 transmitter per cycle
    def collision(self):
        if self.count_writes > 1:
            return True
        else:
            return False

    # Change cycle to verify collision for each time
    def advance_clock(self):
        self.pass_values()

    # Say to transmitter if the medium is idle or busy to transmit
    def sense(self):
        # returns true if channel is busy
        if self.count_writes != 0:
            return True
        else:
            return False