# coding: utf-8
from Frame import Frame
import time
import random
# import Simulator

'''Transmitter info and methods to perform CSMA/CD control'''
class Transmitter:

    def __init__(self, id, medium_ref):

        self.id = id
        self.medium_ref = medium_ref
        self.frame = None
        self.frame_count = 1

    # Send frame to the Medium
    def send(self, message):
        self.message = message
        print("Sending message: " + message.message + " --> " + str(self.id))
        print("Sending at clock ", self.medium_ref.clock)
        time.sleep(0.1)
        self.send_all(message)
        print("Message sent!!")

    # Call all functions to send frames, jam or wait to retransmit
    def send_all(self, frame):
        if self.can_send():
            col = False
            for c in frame.message:
                if not col:
                    print ("Transmitter ", str(self.id), "will send: ", c)
                    self.medium_ref.modify_medium(c)
                    col = self.medium_ref.collision()
                    time.sleep(0.1)
                    print("Collision: ", str(col))
                else:
                    time.sleep(1)
                    print("Jam detected at transmitter " + str(self.id))
                    self.send_jam()
                    frame.collision_count += 1
                    bf = self.calculate_backoff(frame.collision_count)
                    time.sleep(1)
                    print("-------------------------------------")
                    print("Collisions before backoff: ", frame.collision_count)
                    print("Transmitter: ", self.id, " --> Backoff --> Will wait for " + str(bf) + " cycles")
                    print("-------------------------------------")
                    time.sleep(bf * 1)
                    # frame.collision_count += 1
                    self.retry(frame)
                    break

        else:
            print("Transmitter ", self.id, " cannot send")
            # channel busy, wait and send again
            time.sleep(0.1)
            self.send_all(frame)

    # Retransmit the frames if possible and abort if attempts > 16
    def retry(self, frame):
        if frame.collision_count > 16:
            print("16 collisions, abort!")
        else:
            self.send_all(frame)

    # Calculate exponential time to transmitters which collided wait
    def calculate_backoff(self, attempt):
        max_backoff = (2 ** attempt)
        # return np.random.poisson(max_backoff)
        range_values = range(1, max_backoff)
        return random.choice(range_values)

    # Notify the transmitters that a collision had occured
    def send_jam(self):
        # print("Olá! Eu sou um sinal de JAM e vim avisar vocês que ocorreu uma colisão no canal!")
        jam_message = "COLISION"
        for c in jam_message:
            self.medium_ref.modify_medium(c)
            print("Sent char: ", c, " of jam. Transmissor :", str(self.id))
            time.sleep(0.1)
        print("Jam sent!")

    # Verify if media is idle to transmit
    def can_send(self):
        time.sleep(0.1)
        v = self.medium_ref.sense()
        print("Transmitter ", str(self.id), " sensed medium. Can send?: ", str(not v))
        return not v
