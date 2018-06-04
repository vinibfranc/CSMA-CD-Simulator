# coding: utf-8
import numpy as np
from Frame import Frame
import random
# import Simulator

'''Transmitter info and methods to perform CSMA/CD control'''
class Transmitter:

    def __init__(self, id, lamb):

        self.id = id
        self.lambda_number = lamb  # in microseconds
        self.frame = None
        self.status = "Pronto"
        self.backoff_time = 0
        self.transm_start_time = 0
        self.frame_count = 1
        self.current_transm_frame = 0
        self.current_receiver = None

    # Start transmission of frames
    def start_transmission(self, network):
        self.status = "Transmitindo"
        self.current_receiver = self.select_receiver(network)
        self.current_transm_frame = ((abs(network.distance[self.id] - network.distance[self.current_receiver])) * network.distance_between_nodes) / network.speed
        self.frame = Frame(self.frame_count)
        self.transm_start_time = network.current_time

    # Select a receiver to a frame based on a random number and choice
    def select_receiver(self, network):
        random_receiver = range(1, network.transmitter_count + 1)
        #random_receiver.remove(self.id)
        return random.choice(random_receiver)

    # Restart transmission (used when a collision occured and the frame waited its backoff time)
    def restart_transmission(self, current_time):
        self.status = "Transmitindo"
        self.transm_start_time = current_time

    # Stop transmission (used when a collision is detected and all nodes will wait to retransmit)
    def stop_transmission(self, reason='Pronto'):
        self.status = reason

    # Simulates que a availability of a frame (based on Poisson distribution)
    def check_if_frame_available(self):
        return np.random.poisson(self.lambda_number) == 1

    # Calculate que backoff time to all stations when a collision had occured on the medium
    def calculate_backoff_time(self, network):
        self.frame.increment_collision_count()
        # Like Ethernet does, if there are more than 16 collisions of the same frame we abort its transmission
        # many_transmissions = False
        if self.frame.collision_count > 16:
            print("******************************************************************")
            print("Impossível enviar, pois ocorreram muitas colisões do mesmo quadro!")
            print("******************************************************************")
            self.stop_transmission("Muitas colisões!")
            many_transmissions = True

        '''if(many_transmissions):
            self.stop_transmission("Muitas colisões")'''

        # After c collisions, a random number of slot times between 0 and 2^c − 1 is chosen. For the first collision, each sender will wait 0 or 1 slot times. After the second collision, the senders will wait anywhere from 0 to 3 slot times (inclusive). After the third collision, the senders will wait anywhere from 0 to 7 slot times (inclusive), and so forth. As the number of retransmission attempts increases, the number of possibilities for delay increases exponentially.
        random_wait = (2 ** self.frame.collision_count) - 1

        if random_wait > 8:
            random_wait = 8

        self.backoff_time = network.current_time + (np.random.randint(0, high=random_wait) * self.frame.collision_count)

        # self.backoff_time = network.current_time + (np.random.randint(0, high=random_wait) * network.time_slot)
        # self.backoff_time = network.current_time + (np.random.randint(0, high=random_wait) * self.frame.collision_count)
        # self.backoff_time = 2 ** (self.frame.collision_count + (np.random.randint(0, high=random_wait)))

        print("Transmissor:", self.id, "ID do quadro:", self.frame.id, "Quantidade de colisões do quadro:", self.frame.collision_count, "Espera (backoff): ", self.backoff_time)

    # Listen the medium and verifies 4 possibilities on the transmitter
    '''
        1- If the status is Ready and there are frames to transmit, we'll send the frame
        2- If the status is Transmitting and we don't have collisions, the transmitter is Ready to transmit another frame
        3- If the status is Collision, we calculate the backoff and put it to wait this exponencial time
        4- If the status is Many Collisions, we stop the transmissions for the current frame
        5- If the station is waiting and its backoff ends, we try to retransmit the frame
    '''
    def verify_status(self, network):
        if self.status == 'Pronto' and self.check_if_frame_available():
            self.start_transmission(network)

        elif self.status == 'Transmitindo':
            if self.transm_start_time + network.transm_time + self.current_transm_frame < network.current_time:
                self.status = "Pronto"
                self.transm_start_time = 0
                self.current_transm_frame = 0
                self.current_receiver = None
                self.frame_count += 1

        elif self.status == 'Colisão':
            self.calculate_backoff_time(network)
            self.status = 'Esperando'

        elif self.status == 'Esperando' and self.backoff_time <= network.current_time:
            self.restart_transmission(network.current_time)

        elif self.status == 'Muitas colisões':
            self.stop_transmission("Muitas colisões")

    # Measure the efficiency of the algorithm in the simulating condition
    def throughput_analysis(self, network):
        total_time = (self.frame_count - 1) * network.transm_time
        throughput = float((network.transmitter_count - 1) * network.distance_between_nodes * (10 ** 6)) / network.speed
        total_collision_time = network.collision_count * 2 * throughput
        total_send_time = (self.frame_count - 1) * (network.transm_time + throughput)
        try:
            efficiency = float(total_time) / (total_collision_time + total_send_time)
            average_transfer = efficiency * network.bandwidth
        except:
            average_transfer = -1
        return average_transfer