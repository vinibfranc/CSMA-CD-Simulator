# coding: utf-8
from Transmitter import Transmitter
from Medium import  Medium
from Frame import Frame
import time
import collections
import numpy as np
from threading import Thread, Lock

'''Simulate the channel (medium) of transmission of data'''

class Simulator:

    def __init__(self, lambda_number, time_slot, max_time, transmitter_count, distance_between_nodes):

        self.time_slot = time_slot
        self.current_time = 0
        self.transm_time = 10
        self.max_time = max_time
        self.collision_count = 0

        # self.shared_array = shared_array

        self.bandwidth = 100  # Megabits por segundo
        self.speed = 2 * (10 ** 8)
        self.transmitter_count = transmitter_count
        self.distance_between_nodes = distance_between_nodes
        self.distance = collections.defaultdict(int)
        self.transmitter = []
        self.lambda_number = lambda_number

        # Create a shared list of bits that will be the simulation of the shared media (channel)
        '''self.medium_size = 1500
        self.medium = np.zeros(self.medium_size)
        self.medium[:750] = 1
        np.random.shuffle(self.medium)
        print("Meio antes do início: {}".format(self.medium))'''

        # Assign the required number of transmitters and set up a distance between each one
        for i in range(1, self.transmitter_count + 1):
            self.transmitter.append(Transmitter(i, float(self.lambda_number) / self.time_slot, medium))
            self.distance[i] = (i - 1) * self.distance_between_nodes

    '''def modify_medium(self, lock, transmitter_count):
        # arr = Array('i', self.medium)
        lock.acquire()
        # print("Transmissores sensoriando o meio para tentar escrever nele")
        for i in range(1, len(self.medium)):
            if i % 2 == 0:
                self.medium[i] = 0
            else:
                self.medium[i] = 1
        # print(self.medium)
        # print("Transmissor {} tentando escrever no meio!".format(transmitter_count))
        lock.release()'''

    # Run transmissions doing the carrier sensing and collision detection
    def run_transmissions(self):

        for i in range(1, self.transmitter_count + 1):
            self.transmitter[i].verify_status(self)
        self.collision_detection()

        print("-------------------------------------------")
        for i in range(1, self.transmitter_count + 1):
            print("Status do Transmissor {}: {} para {}".format(i, self.transmitter[i].status, self.transmitter[i].current_receiver))
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
            self.send_jam()

    # Notify the transmitters that a collision had occured
    def send_jam(self):
        print("Olá! Eu sou um sinal de JAM e vim avisar vocês que ocorreu uma colisão no canal!")
        for i in range(1, self.transmitter_count + 1):
            # self.transmitter[i].status = "Colisão"
            pass

    # Print basic statistics of the simulation
    def print_statistics(self):
        for i in range(1, t_count + 1):
            print("Total de quadros enviados pelo transmissor {}: {}".format(i, self.transmitter[i].frame_count - 1))
            print("Taxa de transferencia de ponta a ponta média do transmissor {}: {}".format(i, self.transmitter[
                i].throughput_analysis(self)))
        print("Numero de colisoes: ", self.collision_count)
        print("Tempo de simulacao: ", self.current_time)

# Run the simulation

if __name__ == "__main__":
    global medium
    medium = Medium(10)
    # time_sl = 50
    time_sl = 10
    # frame_lambda = 0.5
    frame_lambda = 5
    dist_transmitters = 2000
    delay = ""
    while True:
        try:
            max_time = int(input("Digite o tempo de simulacao (em segundos): "))
            t_count = int(input("Digite a quantidade de transmissores: "))
            # TODO: Method to validate delay
            # delay = eval(input("Ver os quadros sendo enviados em tempo real? (s/n): "))
            simulation = Simulator(frame_lambda, time_sl, max_time, t_count, dist_transmitters)
            break
        except ValueError:
            print("Valor digitado incorretamente! Tente novamente!")
            continue


    for _ in range(max_time):

        lock_st = Lock()

        # p = [0] * simulation.medium_size
        for i in simulation.transmitter:
            a = np.zeros(8)
            frame_message = Frame(1,"asd")
            i.send(frame_message)

            # print(p[i])'''

        #simulation.run_transmissions()
        time.sleep(0.1)
        medium.pass_values()
        '''if delay == "s" or delay == "S":
            time.sleep(1)'''

    simulation.print_statistics()