#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor
from ev3dev2._platform.ev3 import INPUT_1, INPUT_2,INPUT_3,INPUT_4
from ev3dev2.sound import Sound
from time import sleep

import bluetooth
import threading

# booleans of colors to detect
color_Blue=False
color_Green=False
color_Red=False

is_master = True
server_mac = '00:17:E9:B4:CE:E6'

#init sensors from other brick
ts_back_feel = False
ts_left_feel = False
ts_right_feel = False
us_front_dist = 1500

# Connect robot with shared socket
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

# Close the socket
def disconnect(sock):
	sock.close()

# Listen to incoming information via socket
def listen(sock_in):
	global ts_back_feel
	global ts_left_feel
	global ts_right_feel
	global us_front_dist

	while True:
		data = sock_in.readline().rstrip()
		if data.split(',')[0] == 'ts_back':
			ts_back_feel = int(data.split(',')[1])
		if data.split(',')[0] == 'ts_left':
			ts_left_feel = int(data.split(',')[1])
		if data.split(',')[0] == 'ts_right':
			ts_right_feel = int(data.split(',')[1])
		if data.split(',')[0] == 'us_front':
			us_front_dist = float(data.split(',')[1])

#Initialize and start listening mechanism and robot mechanism, parallelized.
#Wait for the robot to reach it's goal and disconnect the listening device.
def run(server_mac, is_master):
	# initialize the sockets
	sock, sock_in, sock_out = connect(server_mac, is_master)

	# make two threads, one to listen to information from socket and one for the robot's movement
	listener = threading.Thread(target=listen, args=(sock_in,))
	runner = threading.Thread(target=main)

	listener.start()
	runner.start()
	
	# wait for runner thread to exit
	runner.join()

	# close all sockets
	disconnect(sock_in)
	disconnect(sock_out)
	disconnect(sock)

# init movements
def drive_forward(tank):
	tank.on(SpeedPercent(25),SpeedPercent(25))

def turn_left(tank):
	tank.on(SpeedPercent(-35),SpeedPercent(35))

def turn_left_slow(tank):
	tank.on(SpeedPercent(-15),SpeedPercent(15))

def turn_right(tank):
	tank.on(SpeedPercent(35),SpeedPercent(-35))

def turn_right_slow(tank):
	tank.on(SpeedPercent(15),SpeedPercent(-15))

def drive_backward(tank):
	tank.on(SpeedPercent(-20),SpeedPercent(-20))


#init movements for missions
def stay_in_box(tank, sensor):
	if(
		sensor == 'cs_left'
		):

		drive_backward(tank)
		sleep(0.400)
		turn_right(tank)
		sleep(0.350)

	if(
		sensor == 'cs_right'
		):

		drive_backward(tank)
		sleep(0.400)
		turn_left(tank)
		sleep(0.300)

	if(
		sensor == 'cs_middle'
		):

		drive_backward(tank)
		sleep(0.400)

	if(
		sensor == 'us_back'
		):

		drive_forward(tank)
		sleep(0.300)


def detect_colors(tank, colorname, sound, measurem):
	tank.stop()
	measurem.on_for_degrees(10,-90,brake=True, block=True)
	measurem.on_for_degrees(15,90, brake=True, block=True)
	print(colorname)
	update_color(tank, colorname, sound)
	drive_backward(tank)
	sleep(0.400)
	turn_left(tank)
	sleep(0.300)

def deal_with_touch(tank, sensor):
	if(
		sensor == 'ts_left'
		):

		drive_backward(tank)
		sleep(0.400)
		turn_right(tank)
		sleep(0.350)

	if(
		sensor == 'ts_right'
		):

		drive_backward(tank)
		sleep(0.400)
		turn_left(tank)
		sleep(0.300)

	if(
		sensor == 'ts_back'
		):

		drive_forward(tank)
		sleep(0.300)
		turn_left(tank)
		sleep(0.300)


def avoid_collision(tank, sensor):
	if(
		sensor == 'us_front'
		):

		turn_right(tank)
		sleep(0.350)



#update color for detectlakes
def update_color(tank, colorname, sound):
	print('in update color')
	global color_Blue
	if colorname == 'Blue':
		print('in color')
		color_Blue = True
		sound.tone(523, 500, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

	global color_Green
	if colorname == 'Green':
		print('in color')
		color_Green = True
		sound.tone(65, 500, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

	global color_Red
	if colorname == 'Red':
		print('in color')
		color_Red = True
		sound.tone(1046, 500, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

	if (
		color_Blue and 
		color_Green and 
		color_Red
		):

		tank.stop()
		sound.speak('all lakes detected', volume = 1000, play_type = Sound.PLAY_WAIT_FOR_COMPLETE)

def main():
	sound = Sound()
	tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
	measurem = Motor(OUTPUT_B)

	cs_left = ColorSensor(INPUT_1)
	cs_middle = ColorSensor(INPUT_2)
	cs_right = ColorSensor(INPUT_3)
	us_back = UltrasonicSensor(INPUT_4)

	while (
		not color_Blue or 
		not color_Green or 
		not color_Red
		):
		cs_left_color = cs_left.color_name
		cs_middle_color = cs_middle.color_name
		cs_right_color = cs_right.color_name
		us_back_dist = us_back.distance_centimeters
		if (
			cs_left_color == 'White'
			):
	
			stay_in_box(tank_drive,'cs_left')
			continue
	
		if (
			cs_right_color == 'White'
			):
	
			stay_in_box(tank_drive,'cs_right')
			continue
	
		if (
			cs_middle_color == 'White'
			):
	
			stay_in_box(tank_drive,'cs_middle')
			continue
	
		if (
			us_back_dist > 5
			):
	
			stay_in_box(tank_drive,'us_back')
			continue
	
		# if rover in correct position to sample
		# middle sensor good
		if (
			cs_middle_color == 'Blue' or 
			cs_middle_color == 'Green' or 
			cs_middle_color == 'Red'
			):
			# also right sensor good
			if (
				cs_right_color == 'Blue' or 
				cs_right_color == 'Green' or 
				cs_right_color == 'Red'
				):
	
				detect_colors(tank_drive,cs_middle_color, sound, measurem)
				continue
	
		#if rover not in correct position but has detected colour
		if( 
			cs_left_color == 'Blue' or 
			cs_left_color == 'Green' or 
			cs_left_color == 'Red' or 
			cs_middle_color == 'Blue' or 
			cs_middle_color == 'Green' or 
			cs_middle_color == 'Red'
			):
	
			turn_left_slow(tank_drive)
			continue
	
	
		if( 
			cs_right_color == 'Blue' or 
			cs_right_color == 'Green' or 
			cs_right_color == 'Red'
			):
	
			turn_right_slow(tank_drive)
			continue
	
	
		if( 
			ts_left_feel == 1
			):
	
			deal_with_touch(tank_drive,'ts_left')
			continue
	
		if( 
			ts_right_feel == 1
			):
	
			deal_with_touch(tank_drive,'ts_right')
			continue
	
		if( 
			ts_back_feel == 1
			):
	
			deal_with_touch(tank_drive,'ts_back')
			continue
	
		if( 
			us_front_dist <= 15
			):
	
			avoid_collision(tank_drive,'us_front')
			continue
	
		drive_forward(tank_drive)

run(server_mac, is_master)
