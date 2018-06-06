# coding: utf-8
from Transmitter import Transmitter
from Medium import Medium
from Frame import Frame
import time
import sys
from threading import Thread, Lock

'''Simulate the channel (medium) of transmission of data'''
class Simulator:

    def __init__(self, transmitter_count):
        self.transmitter_count = transmitter_count
        self.transmitter = []
        for i in range(1, self.transmitter_count + 1):
            self.transmitter.append(Transmitter(i,  medium))

    #Print basic statistics of the simulation
    '''def print_statistics(self):
        for i in range(1, t_count + 1):
            print("Total de quadros enviados pelo transmissor {}: {}".format(i, self.transmitter[i].frame_count - 1))
            print("Taxa de transferência de ponta a ponta média do transmissor {}: {}".format(i, self.transmitter[
                i].throughput_analysis(self)))
        print("Numero de colisoes: ", self.collision_count)
        print("Tempo de simulacao: ", self.current_time)'''

# Will be a thread that update medium for each cycle
def run_sim(m):
    print("Simulation started")
    for i in range(500):
        time.sleep(0.1)
        medium.advance_clock()
    print("Simulation completed")
    sys.exit()

# Run the simulation
if __name__ == "__main__":
    global medium
    time_sl = 10
    medium = Medium(time_sl)
    while True:
        try:
            t_count = int(input("Type the number of transmitters: "))
            simulation = Simulator(t_count)
            break
        except ValueError:
            print("Incorrect input! Try again")
            continue

    threads = []
    medium.advance_clock()
    for device in simulation.transmitter:
        frame_message = Frame(1,"message")
        t = Thread(target=device.send, args=(frame_message,))
        threads.append(t)
        # t.start()

    print("ok")

    mt = Thread(target=run_sim, args=(medium,))
    mt.start()


    for t in threads:
        t.start()
    # mt.join()

    print("ok3")
    time.sleep(2)
    print("ok4")