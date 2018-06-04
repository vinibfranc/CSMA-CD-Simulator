# coding: utf-8
'''Frame simplified information'''
class Frame:
    def __init__(self, id, message):
        self.id = id
        self.collision_count = 0
        self.message = message
        self.size = len(message)

    def increment_collision_count(self):
        self.collision_count += 1