from bouncy_shots import start_play
from controller_data_recording import start_collecting_data
import threading
from multiprocessing import Process, Value, Array

if __name__ == '__main__':

    p1 = Process(target=start_play)
    p2 = Process(target=start_collecting_data)

    p1.start()
    p2.start()

    p1.join()
    p2.join()