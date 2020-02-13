import RPi.GPIO as GPIO
import numpy as np
import time

SLEEPTIME = 0.1
WINDOWSIZE = 5
#trig's must be seperate
TRIG1 = 4
#TRIG2 = 2

#echo's can be shared??
ECHO1 = 14
#ECHO2 = 3

#TRIG1 = 23
#ECHO1 = 24
#TRIG2 = 20
#ECHO2 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
#GPIO.setup(TRIG2, GPIO.OUT)
#GPIO.setup(ECHO2, GPIO.IN)


def running_mean(x, N):
	cumsum = np.cumsum(np.insert(x, 0, 0))
	return (cumsum[N:] - cumsum[:-N]) / float(N)


def getDist(trig, echo, name):
	GPIO.output(trig, False)
	
	#print "Waiting for sensor to settle"
	time.sleep(SLEEPTIME)
	GPIO.output(trig, True)           #sending pulse that will bounce off object to be measured
	time.sleep(0.00001)
#        time.sleep(0.001)
	GPIO.output(trig, False)
		
	while GPIO.input(echo)==0:        #timing how long sound wave takes to return
		pulse_start = time.time()
	while GPIO.input(echo)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	inchDist = distance/2.54
	return inchDist
#	print ("Distance for sensor %s: %.2f cm\t %.2f in\t %.2f ft" %(name, distance, inchDist, inchDist/12))
#	print ("%s: %.2f ft" %(name, inchDist/12))


try:
	dist1 = []
	dist1.append(0)
#        print(running_mean([1,2,3], 1))
	while True:
		currDist = getDist(TRIG1, ECHO1, "one")
		if(currDist < 20*12):
			dist1.append(currDist)
			currLen = len(dist1)
			mean = running_mean(dist1[currLen-WINDOWSIZE:currLen], WINDOWSIZE)
#                print(mean/12)
			if (len(mean) != 0):
				print ("%.2f ft" %(mean[0]/12))

except KeyboardInterrupt:
	print("Cleaning up 2")
	GPIO.cleanup()

