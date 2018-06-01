# coding: utf-8
from Transmitter import Transmitter
import time
import collections
from multiprocessing import Process, Lock  # not using multithreading because it doesn't provide real parallelism

'''Simulate the channel (medium) of transmission of data'''


class Simulator:

    def __init__(self, lambda_number, time_slot, max_time, transmitter_count, distance_between_nodes):

        self.time_slot = time_slot
        self.current_time = 0
        self.transm_time = 10
        self.max_time = max_time
        self.collision_count = 0
        self.bandwidth = 100  # Megabits por segundo
        self.speed = 2 * (10 ** 8)
        # self.whichNodes = []
        self.transmitter_count = transmitter_count
        self.distance_between_nodes = distance_between_nodes
        self.distance = collections.defaultdict(int)
        self.transmitter = [-1]
        self.lambda_number = lambda_number

        # Assign the required number of transmitters and set up a distance between each one
        for i in range(1, self.transmitter_count + 1):
            self.transmitter.append(Transmitter(i, float(self.lambda_number) / self.time_slot))
            self.distance[i] = (i - 1) * self.distance_between_nodes

    # Run transmissions doing the carrier sensing and collision detection
    def run_transmissions(self):
        # def run(self, lock):

        # TODO: Made processes lock works
        # self.create_threads()

        # Made possible events and detect collisions
        for i in range(1, self.transmitter_count + 1):
            # Lock medium
            # lock.acquire()
            self.transmitter[i].carrier_sensing(self)
            # Unlock medium
            # lock.release()
        self.collision_detection()

        for i in range(1, self.transmitter_count + 1):
            print("Status do Transmissor {}: {} para {}".format(i, self.transmitter[i].status,
                                                                self.transmitter[i].current_receiver))
        print("-------------------------------------")
        self.current_time = self.current_time + 1

        print("Tempo: {} s".format(self.current_time))

    '''def create_threads(self):
        lock_st = Lock()
        for i in range(1, self.nodeCount + 1):
            #Process(target=self.run, args=(self, lock)).start()
            Process(target=self.run, args=lock_st.start())
            print("Status of Node {}: {} to {}".format(i, self.node[i].status, self.node[i].curReceiver))
            print("-------------------------------------")
        self.cur_time = self.cur_time + 1'''

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
    # def send_jam(self, transmitter):
    def send_jam(self):
        print("Olá! Eu sou um sinal de JAM! Ocorreu uma colisão!")
        '''for i in range(1, self.transmitter_count + 1):
            transmitter.status = "Esperando"'''
        # TODO: Stop transmissions by all stations (change all status to Waiting)

    # Print basic statistics of the simulation
    def print_statistics(self):
        for i in range(1, t_count + 1):
            print("Total de quadros enviados pelo transmissor {}: {}".format(i, self.transmitter[i].frame_count - 1))
            print("Taxa de transferência de ponta a ponta média do transmissor {}: {}".format(i, self.transmitter[
                i].throughput_analysis(self)))
        print("Numero de colisoes: ", self.collision_count)
        print("Tempo de simulacao: ", self.current_time)


# Run the simulation
if __name__ == "__main__":
    # time_sl = 50
    time_sl = 10
    # frame_lambda = 0.5
    frame_lambda = 5
    dist_transmitters = 2000
    max_time = int(input("Digite o tempo de simulação (em segundos): "))
    t_count = int(input("Digite a quantidade de transmissores: "))
    delay = input("Ver os envio com delay? (s/n): ")
    simulation = Simulator(frame_lambda, time_sl, max_time, t_count, dist_transmitters)
    for _ in range(max_time):
        # while True:
        simulation.run_transmissions()
        if delay == "s":
            time.sleep(1)
    simulation.print_statistics()
