import os
import glob
import time
import logging


class one_wire_init():
	os.system('modprobe w1-gpio') #attach 1-wire modules to the kernel
	os.system('modprobe w1-therm')

	device_file='0'
	try:
		base_dir = '/sys/bus/w1/devices/'	#1-wire devices detected here
		device_folder = glob.glob(base_dir + '28*')[0] #match folders(devices) starting w/28 ()
		device_file = device_folder + '/w1_slave'
	except Exception, e:
		logging.debug('Error in 1-wire driver: (no device found?) %s' % e)

def read_temp_raw():
	f = open(one_wire_init.device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	#print(lines)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
	lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	#print(equals_pos)
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c