# coding: utf-8
from Transmitter import Transmitter
from Medium import Medium
from Frame import Frame
import time
import collections
import numpy as np
from threading import Thread, Lock

'''Main class that executes the simulation'''
class Simulator:

    def __init__(self, transmitter_count):
        self.transmitter_count = transmitter_count
        self.transmitter = []
        for i in range(1, self.transmitter_count + 1):
            self.transmitter.append(Transmitter(i, medium))

    # Run transmissions doing the carrier sensing and collision detection
    '''def run_transmissions(self):

        for i in range(1, self.transmitter_count + 1):
            self.transmitter[i].verify_status(self)
        self.collision_detection()

        print("-------------------------------------------")
        for i in range(1, self.transmitter_count + 1):
            print("Estado do Transmissor {}: {} para {}".format(i, self.transmitter[i].status,
                                                                self.transmitter[i].current_receiver))
        print("-------------------------------------------")
        self.current_time = self.current_time + 1

        print("Tempo: {} s".format(self.current_time))

    # If there is only one station transmitting at a time, that's ok
    # But if there are more, we have a collision and a jam signal are send to all transmitters
    def collision_detection(self):
        active_transmitters = []
        for i in range(1, self.transmitter_count + 1):
            if self.transmitter[i].status == "Transmitindo":
                active_transmitters.append(i)
        if len(active_transmitters) >= 2:
            self.collision_count = self.collision_count + 1
            for i in active_transmitters:
                self.transmitter[i].stop_transmission("Colisão")
            self.send_jam()'''


def run_sim(m):
    for i in range(5000):
        time.sleep(0.1)
        medium.advance_clock()
    print("ok2")


# Run the simulation
if __name__ == "__main__":
    global medium
    medium = Medium(10)
    time_sl = 10
    frame_lambda = 5
    dist_transmitters = 2000
    # delay = ""
    while True:
        try:
            t_count = int(input("Digite a quantidade de transmissores: "))
            simulation = Simulator(t_count)
            break
        except ValueError:
            print("Valor digitado incorretamente! Tente novamente!")
            continue

    threads = []
    for device in simulation.transmitter:
        frame_message = Frame(1, "101010")
        # Thread(target=device.send, args=(frame_message,)).start()
        t = Thread(target=device.send, args=(frame_message,))
        threads.append(t)
        t.start()
        # device.send(frame_message)

    print("ok")

    mt = Thread(target=run_sim, args=(medium,))
    mt.start()

    for t in threads:
        t.join()
    mt.join()

    print("ok3")
    time.sleep(10)
    print("ok4")
