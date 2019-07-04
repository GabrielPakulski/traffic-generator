import sys
import argparse
import socket
import math
import time

DATAGRAM_SIZE = 1500

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
        rate_in_bytes = arguments.r * 1000/8 #Transforma kbit/s -> bytes/s
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dest = (HOST,PORT)

        rate_in_datagrams = math.ceil(rate_in_bytes / DATAGRAM_SIZE)

        print("Executando o gerador de tráfego a:", rate_in_bytes*8/1000000,"Mbits/s")

        message = bytes(DATAGRAM_SIZE)

        sleep_timer = 1.0 / float(rate_in_datagrams)

        # Pega o tempo de envio de uma mensagem
        t_start = time.time()
        udp.sendto(message,dest)
        t_end = time.time()

        #Desconta o atraso de envio
        sleep_timer = sleep_timer - (t_end - t_start)

        while True:
                time.sleep(sleep_timer)
                udp.sendto(message,dest)



if __name__ == '__main__':
    main()
