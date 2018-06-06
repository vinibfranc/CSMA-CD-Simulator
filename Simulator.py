# coding: utf-8

from Transmitter import Transmitter
from Medium import Medium
from Frame import Frame
import time
import sys
from threading import Thread

'''Simulate the CSMA/CD process using Threads and and a shared Medium'''
class Simulator:

    def __init__(self, transmitter_count):
        self.transmitter_count = transmitter_count
        self.transmitter = []
        for i in range(1, self.transmitter_count + 1):
            self.transmitter.append(Transmitter(i, medium))


def run_sim(m):
    print("Simulacao iniciada!")
    for i in range(500):
        time.sleep(0.1)
        medium.advance_clock()
    print("Simulacao concluida!")
    sys.exit()

# Run the simulation with user input of transmitter number
if __name__ == "__main__":
    global medium
    time_sl = 10
    medium = Medium(10)
    while True:
        try:
            t_count = int(input("Digite a quantidade de transmissores: "))
            simulation = Simulator(t_count)
            break
        except ValueError:
            print("Valor digitado incorretamente! Tente novamente!")
            continue

    threads = []
    medium.advance_clock()
    for device in simulation.transmitter:
        frame_message = Frame(1, "asd")
        t = Thread(target=device.send, args=(frame_message,))
        threads.append(t)
        # t.start()

    print("ok2!")

    mt = Thread(target=run_sim, args=(medium,))
    mt.start()

    for t in threads:
        t.start()
    # mt.join()

    print("ok3!")
    time.sleep(10)
    print("ok4!")
