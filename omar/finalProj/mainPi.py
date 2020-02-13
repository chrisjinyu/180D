### make so pings sensors in background and doesnt wait constantly for server's comms
### make comms independent of game


import RPi.GPIO as GPIO
import numpy as np
import time
import board
import neopixel
import socket 

SLEEPTIME = 0.1  #time for dist to wait - maybe set to 0??
MEANWINDOWSIZE = 5  #size of running average window - relate to sleeptime

RED = 0 #red light output
GREEN = 1 # green light output
WARNING = 2 #warning for when getting close to moving too much
FAULT = 3 #when player has moved too much and must go back

TRIG1 = 4
TRIG2 = 2
ECHO = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)

pixels = neopixel.NeoPixel(board.D18, 12)
player1dists = []
player1dists.append(0)
Dist1 = 0
player2dists = []
player2dists.append(0)
Dist2 = 0

def running_mean(x, N):
	cumsum = np.cumsum(np.insert(x, 0, 0))
	return (cumsum[N:] - cumsum[:-N]) / float(N)

def getDistHelper(trig, echo):
	#GPIO.output(trig, False)
	#time.sleep(SLEEPTIME)
	GPIO.output(trig, True)           #sending pulse that will bounce off object to be measured
	time.sleep(0.00001)
	GPIO.output(trig, False)

	while GPIO.input(echo) == 0:        #timing how long sound wave takes to return
		pulse_start = time.time()
	while GPIO.input(echo) == 1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	inchDist = distance/2.54
	return inchDist

def getDist():
	#while True:	
		Dist1 = 0
		currDist = getDistHelper(TRIG1, ECHO) 
		if(currDist < 20*12):
			player1dists.append(currDist)
		currLen = len(player1dists)
		mean1 = running_mean(player1dists[currLen-MEANWINDOWSIZE:currLen], MEANWINDOWSIZE)
		if (len(mean1) != 0): 
			Dist1 = mean1[0]
		#	print("Dist1 : " + str(Dist1))
		#else: print("len mean 1 is 0")
		
		Dist2 = 0
		currDist = getDistHelper(TRIG2, ECHO)
		if(currDist < 20*12):
			player2dists.append(currDist)
		currLen = len(player2dists)
		mean2 = running_mean(player2dists[currLen-MEANWINDOWSIZE:currLen], MEANWINDOWSIZE)
		if (len(mean2) != 0): 
			Dist2 = mean2[0]
		#	print("Dist2: " + str(Dist2))
		#else: print("len mean 2 is 0")
	
	#if(len(mean1) != 0 && len(mean2) != 0):
	#	break
		return (str(Dist1) + ',' +  str(Dist2))
	
def changeLight(color): # maybe add winning/resetting sequence(s)
	#change the light to red or green
	if (color == 0):
		pixels.fill((255,0,0))
	elif (color == 1):
		pixels.fill((0,255,0))
	elif (color == 2): 
		print("not supported (yet?) \n")
	elif (color == 3):
		print("not supported (yet?) \n")
	else:
		print("invalid input to changeLight!\n")
		
	
	
if __name__ == "__main__": 
	#print "Executed when invoked directly"
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(('192.168.1.8', 808))
		#client.send("I AM CLIENT\n".encode())
#		from_server = client.recv(4096).decode()
		#print(from_server)
		while 1:
			#print("d")
			dataToSend = getDist()
#			print("dist1: %d\t dist2: %d" %(Dist1, Dist2))
#			dataToSend = str(Dist1) + ',' + str(Dist2)
			#print("e")
			#print(dataToSend)
			#print("f")
			client.send(dataToSend.encode())
			
			#print("a")
			dataRec = client.recv(4096).decode()
			#print("b")
			#print(dataRec)
			if dataRec:  #server should send RED, GREEN, WARNING, FAULT, etc.
				changeLight(int(dataRec))
			#print("c")
		
	except KeyboardInterrupt:
		print("\nCleaning up\n")
	except BrokenPipeError:
		print("\nBroken Pipe!\n")
	finally:
		pixels.fill((0,0,0))
		GPIO.cleanup()
		client.close()
#	changeLight(RED)
#	while 1:
		#change light red to green and back and measure dist of players
#		startPlayer1Dist = getDist(1)
#		startPlayer2Dist = getDist(2)



#else: 
	#print "Executed when imported"

