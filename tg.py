import sys
import argparse
import socket
import math
import time

DATAGRAM_SIZE = 1500*8

def main():
    parser = argparse.ArgumentParser(description='Gerador de tráfego')
    parser.add_argument("-i", type=str)
    parser.add_argument("-p", type=int)
    parser.add_argument("-r", type=int)
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
        rate_in_bits = arguments.r * 1000 #Transforma kbit/s -> bit/s
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dest = (HOST,PORT)

        rate_in_Mbits = rate_in_bits / 1000000 #Transforma bit -> Mbit/s
        rate_in_datagrams = math.ceil(rate_in_bits / DATAGRAM_SIZE)

        print("Executando o gerador de tráfego a:", rate_in_Mbits,"Mbits/s")
        # print("Rajada",rate_in_bits,"bits/s")
        # print("Taxa:", rate_in_datagrams, "datagrams per second")
        # print("Datagrams/s * Datagram size =", rate_in_datagrams*DATAGRAM_SIZE, "bits/s")

        message = bytes(DATAGRAM_SIZE)

        sleep_timer = 1.0 / float(rate_in_datagrams)
        # print("Sleep for :",sleep_timer)

        # Pega o tempo de envio de uma mensagem
        t_start = time.time()
        udp.sendto(message,dest)
        t_end = time.time()

        #Desconta o atraso de envio
        sleep_timer = sleep_timer - (t_end - t_start)
        # print("Sleep for :",sleep_timer)
        sleep_timer = sleep_timer/1.125

        while True:
                udp.sendto(message,dest)
                time.sleep(sleep_timer)


if __name__ == '__main__':
    main()
