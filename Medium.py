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

    # Control the modifications on medium to detect collisions
    def modify_medium(self, val):
        self.last_medium = val
        self.count_writes += 1
        print("Medium modified at clock: ", str(self.clock), " count: ", str(self.count_writes))

    def pass_values(self):
        self.first_medium = self.last_medium
        self.last_medium = np.zeros(self.medium_size)
        self.last_writes = self.count_writes
        self.count_writes = 0
        self.clock += 1

    # Collision detection occurs when more than one changes medium at this final
    def collision(self):
        print("Collision count ", str(self.count_writes))
        if self.last_writes > 1:
            return True
        else:
            return False

    # For each cycle detect if a collision occured (called by a thread)
    def advance_clock(self):
        print("Clock advanced, writes: ", str(self.count_writes))
        self.pass_values()

    # Notify the station if medium is idle or busy
    def sense(self):
        # returns true if channel is busy
        if self.last_writes != 0:
            return True
        else:
            return False