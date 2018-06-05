# coding: utf-8
import numpy as np
'''Frame simplified information'''
class Frame:
    def __init__(self, id, message):
        self.id = id
        self.collision_count = 0
        self.message = message
        self.size = len(message)

        '''self.message = np.zeros(8)
        self.message[:4] = 1
        np.random.shuffle(self.message)'''

    def increment_collision_count(self):
        self.collision_count += 1