# coding: utf-8
'''Frame simplified information'''
class Frame:
    def __init__(self, id, size=1000):
        self.id = id
        self.size = size
        self.collision_count = 0

    def increment_collision_count(self):
        self.collision_count += 1
