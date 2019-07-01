import sys
import argparse
import socket
import math
import time

DATAGRAM_SIZE = 1500*8

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="IP destino", type=str)
    parser.add_argument("-p", help="Porta", type=int)
    parser.add_argument("-r", help="Tamanho da rajada", type=int)
    arguments = parser.parse_args()

    if(arguments.i == None):
        print("Falta o IP destino")
    if(arguments.p == None):
        print("Falta a Porta destino")
    if(arguments.r == None):
        print("Falta o tamanho da rajada")
    else:

        HOST = arguments.i
        PORT = arguments.p
        burst = arguments.r * 1000
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dest = (HOST,PORT)

        rate_in_Mbits = burst / 1000000
        rate_in_datagrams = math.ceil(burst / DATAGRAM_SIZE)

        print("Rajada",burst,"bits/s")
        print("Taxa:", rate_in_Mbits,"Mbits/s")
        print("Taxa:", rate_in_datagrams, "datagrams per second")
        print("Datagrams/s * Datagram size =", rate_in_datagrams*DATAGRAM_SIZE, "bits/s")

        message = bytearray(DATAGRAM_SIZE)

        sleep_timer = 1.0 / float(rate_in_datagrams)
        print("Sleep for :",sleep_timer)
        t_start = time.time()
        udp.sendto(message,dest)
        t_end = time.time()
        sleep_timer = sleep_timer - (t_end - t_start)
        print("Sleep for :",sleep_timer)
        sleep_timer = sleep_timer/1.125

        while True:
            for packet in range(0,rate_in_datagrams):
                udp.sendto(message,dest)
                time.sleep(sleep_timer)






if __name__ == '__main__':
    main()
