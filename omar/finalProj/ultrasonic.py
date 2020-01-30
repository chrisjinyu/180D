import RPi.GPIO as GPIO
import time

#trig's must be seperate
TRIG1 = 4
TRIG2 = 2

#echo's can be shared??
ECHO1 = 14
ECHO2 = 3

#TRIG1 = 23
#ECHO1 = 24
#TRIG2 = 20
#ECHO2 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

def getDist(trig, echo, name):
	GPIO.output(trig, False)
	
	#print "Waiting for sensor to settle"
	time.sleep(0.5)
	GPIO.output(trig, True)           #sending pulse that will bounce off object to be measured
	time.sleep(0.00001)
	GPIO.output(trig, False)
		
	while GPIO.input(echo)==0:        #timing how long sound wave takes to return
		pulse_start = time.time()
	while GPIO.input(echo)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	inchDist = distance/2.54
	print ("Distance for sensor %s: %.2f cm\t %.2f in\t %.2f ft" %(name, distance, inchDist, inchDist/12))
	
try:
	while True:
		getDist(TRIG1, ECHO1, "one")
		getDist(TRIG2, ECHO2, "two")
except KeyboardInterrupt:
	print("Cleaning up 2")
	GPIO.cleanup()

