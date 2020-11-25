#!/usr/bin/python3

from time import sleep

import bluetooth
import threading

IS_MASTER = True
# IS_MASTER = False
SERVER_MAC = 'CC:78:AB:50:B2:46'
NUMBER_OF_ACTIONS = 5


def connect(server_mac, is_master=True):
    """

    @param server_mac: MAC address of the master brick
    @param is_master: determines which brick acts as the server and waits for the other brick to connect
    @return: the communication socket between slave and master, the read socket file object and write socket file object
    """
    port = 3
    if is_master:
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind((server_mac, port))
        server_sock.listen(1)
        print('Listening...')
        client_sock, address = server_sock.accept()
        print(f'Accepted connection from {address}')
        return client_sock, client_sock.makefile('r'), client_sock.makefile('w')
    else:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print('Connecting...')
        sock.connect((server_mac, port))
        print('Connected to ', server_mac)
        return sock, sock.makefile('r'), sock.makefile('w')


def disconnect(sock):
    """
    wrapper for closing sockets or socket file objects
    @param sock: socket or file object to be closed
    """
    sock.close()


def run(server_mac, is_master=True, number_of_actions=5):
    """
    main function of the application. Starts the Bluetooth threads, does work in the main thread.
    After the main thread has finishes "Doing something" closes the Bluetooth threads and disconnects the sockets
    @param server_mac: MAC address of the master brick
    @param is_master: determines which brick acts as the server and waits for the other brick to connect
    @param number_of_actions:
    """
    sock, sock_in, sock_out = connect(server_mac, is_master)
    listener = threading.Thread(target=start_listening if is_master else listen,
                                args=(sock_in, sock_out, number_of_actions))
    listener.start()
    for i in range(number_of_actions):
        print(f'[{str(i)}] Doing something...')
        sleep(1)
    listener.join()
    disconnect(sock_in)
    disconnect(sock_out)
    disconnect(sock)


def start_listening(sock_in, sock_out, number_of_actions):
    """
    Function that writes the first message (e.g, should be done by the master) before going to the listen function
    @param sock_in: socket file object used for reading data
    @param sock_out: socket file object used for writing data
    @param number_of_actions: number of expected integer to be sent and received
    """
    i = 1
    sock_out.write(f'{str(i)}\n')
    sock_out.flush()
    print(f'Sent {str(i)}')
    listen(sock_in, sock_out, number_of_actions)


def listen(sock_in, sock_out, number_of_actions):
    """
    Function that wait for a message from other party, increments the received integer and sends the result
    @param sock_in: socket file object used for reading data
    @param sock_out: socket file object used for writing data
    @param number_of_actions: number of expected integer to be sent and received
    """
    print('Now listening...')
    stop_listening = False
    while not stop_listening:
        data = int(sock_in.readline())
        print(f'Received {str(data)}')
        if data == -1:
            print('Received stop from other party')
            break
        elif data == number_of_actions:
            print('Received last message, sending stop to other party')
            stop_listening = True
            data = -1
        else:
            data += 1
        sleep(1)
        sock_out.write(f'{str(data)}\n')
        sock_out.flush()
        print(f'Sent {str(data)}')


run(SERVER_MAC, IS_MASTER, NUMBER_OF_ACTIONS)
