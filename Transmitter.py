# coding: utf-8
import numpy as np
from Frame import Frame
import random
# import Network

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
    def start_transmission(self, station):
        self.status = "Transmitindo"
        self.current_receiver = self.select_receiver(station)
        self.current_transm_frame = ((abs(station.distance[self.id] - station.distance[self.current_receiver])) * station.distanceBetweenNodes) / station.vel
        self.frame = Frame(self.frame_count)
        self.transm_start_time = station.current_time

    #TODO: Generate real random number

    # Select a receiver to a frame based on a random number and choice
    def select_receiver(self, station):
        random_receiver = range(1, station.frame_count)
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
    def calculate_backoff_time(self, station):
        self.frame.increment_collision_count()
        attempt = (2 ** self.frame.collision_count) - 1

        if attempt > 8:
            attempt = 8
            print("Impossível enviar, pois ocorreram muitas colisões do mesmo pacote!")

        self.backoff_time = station.current_time + (np.random.randint(0, high=attempt) * station.time_slot)
        print("Transmissor:", self.id, "ID do quadro:", self.frame.id, "Quantidade de colisões do pacote:", self.frame.collision_count, " backoff = ", self.backoff_time)

    # Listen the medium and verifies 4 possibilities on the transmitter
    '''
        1- If the status is Ready and there are frames to transmit, we'll send the frame
        2- If the status is Transmitting and we don't have collisions, the transmitter is Ready to transmit another frame
        3- If the status is Collision, we calculate the backoff and put it to wait this exponencial time
        4- If the station is waiting and its backoff ends, we try to retransmit the frame
    '''
    def carrier_sensing(self, station):
        if self.status == 'Pronto' and self.check_if_frame_available():
            self.start_transmission(station)

        elif self.status == 'Transmitindo':
            if self.transm_start_time + station.tt + self.current_transm_frame < station.current_time:
                self.status = "Pronto"
                self.transm_start_time = 0
                self.current_transm_frame = 0
                self.current_receiver = None
                self.frame_count += 1

        elif self.status == 'Colisão':
            self.calculate_backoff_time(station)
            self.status = 'Esperando'

        elif self.status == 'Esperando' and self.backoff_time <= station.current_time:
            self.restart_transmission(station.current_time)

    # Here we measure the efficiency of the algorithm in the simulating condition
    def throughput_analysis(self, station):
        pass
        '''total_tt = (self.frame_count - 1) * station.tt
        tp = float((station.distance[station.frame_count] - station.distance[1])
                   * station.distanceBetweenNodes) / station.vel
        total_collision_time = station.collCount * 2 * tp
        total_send_time = (self.frame_count - 1) * (station.tt + tp)
        try:
            efficiency = float(total_tt)/(total_collision_time + total_send_time)
            th = efficiency * station.bandwidth
        except:
            th = -1
        return th'''

# n = Frame(1, 0.5)

