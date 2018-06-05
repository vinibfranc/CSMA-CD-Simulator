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

    def modify_medium(self, val):
        self.last_medium = val
        self.count_writes += 1

    def pass_values(self):
        self.first_medium = self.last_medium
        self.last_medium = np.zeros(self.medium_size)
        self.count_writes = 0

    def collision(self):
        if self.count_writes > 1:
            return True
        else:
            return False

    def advance_clock(self):
        self.pass_values()

    def sense(self):
        # returns true if channel is busy
        if self.count_writes != 0:
            return True
        else:
            return False