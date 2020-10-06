#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor
from ev3dev2._platform.ev3 import INPUT_1, INPUT_2,INPUT_3,INPUT_4
from time import sleep

import bluetooth

is_master = False
server_mac = '00:17:E9:B4:CE:E6'

ts_back = TouchSensor(INPUT_1)
ts_left = TouchSensor(INPUT_2)
ts_right = TouchSensor(INPUT_3)
us_front = UltrasonicSensor(INPUT_4)

# initialize the sockets
def connect(server_mac, is_master):
	port = 3
	if is_master:
		server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		server_sock.bind((server_mac, port))
		server_sock.listen(1)
		print('Listening...')
		client_sock, address = server_sock.accept()
		print('Accepted connection from ', address)
		return client_sock, client_sock.makefile('r'), client_sock.makefile('w')		
	else:
		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		print('Connecting...')
		sock.connect((server_mac, port))
		print('Connected to ', server_mac)
		return sock, sock.makefile('r'), sock.makefile('w')

def disconnect(sock):
	sock.close()

def talk(sock_out, sensor, value):
	sock_out.write(sensor + ',' + str(value) + '\n')
	sock_out.flush()

def run(server_mac, is_master):
	sock, sock_in, sock_out = connect(server_mac, is_master)
	
	while True:
		talk(sock_out, 'ts_back', ts_back.is_pressed)
		talk(sock_out, 'ts_left', ts_left.is_pressed)
		talk(sock_out, 'ts_right', ts_right.is_pressed)
		talk(sock_out, 'us_front', us_front.distance_centimeters)
	
	disconnect(sock_in)
	disconnect(sock_out)
	disconnect(sock)

run(server_mac, is_master)
