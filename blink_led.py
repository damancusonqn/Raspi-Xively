import RPi.GPIO as GPIO ## Import GPIO library
import time
#GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setmode(GPIO.BCM) ##Use BCM pin Names
GPIO.setup(18, GPIO.OUT) ## Setup GPIO Pin 18 to OUT (LED)
GPIO.output(18,GPIO.HIGH) ## Turn on GPIO pin 18 

while(1):
	GPIO.output(18,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(18,GPIO.LOW)
	time.sleep(0.1)
# The same script as above but using BCM GPIO 00..nn numbers

#GPIO.setup(17, GPIO.IN)
#GPIO.setup(18, GPIO.OUT)
#input_value = GPIO.input(17)
#GPIO.output(18, GPIO.HIGH)