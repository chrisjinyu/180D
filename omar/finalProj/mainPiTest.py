import speech_recognition as sr
import socket
import sys
import random
import time

P1MIC_INDEX = 0 ##calibrate for computer !!!
P2MIC_INDEX = 1 

RAND_LOW = 1
RAND_HIGH = 2
FORGIVE_TIME = 0.25 #time after light goes red to forgive movement


RED = 0#.encode() #red light output
GREEN = 1#.encode() # green light output
WARNING = 2#.encode() #warning for when getting close to moving too much
FAULT = 3#.encode() #when player has moved too much and must go back


r1=sr.Recognizer()
r1.dynamic_energy_adjustment_ratio =  2

distances = [] ##needed??
	
		
def listen(playerNum):
	#call either of Neil's codes depending on which player
	if (playerNum == 1):
		INDEX = P1MIC_INDEX
	elif (playerNum == 2):
		INDEX = P2MIC_INDEX
	else:
		print("invalid playerNum")

	try:
		with sr.Microphone(device_index=INDEX) as source:
			r1.adjust_for_ambient_noise(source,duration=5)
			r1.energy_threshold = 4000
			print('Listening... ')
			audio= r1.listen(source, timeout=5)
			print ("processing...")
			#try:
			recog = r1.recognize_google(audio)
			if 'true' in recog:
				print("Player %i said True" % (playerNum))
			elif 'false' in recog:
				print("Player %i said False" % (playerNum))
			else:
				print('You said: {}'.format(recog))
			#except sr.UnknownValueError:
			#    print('unknown value error')
			#except sr.RequestError as e:
			#    print('failed'.format(e))
			#except sr.WaitTimeoutError:
			#    print('nothing heard before the timeout')
#			with open ('rec2.wav', 'wb') as f:
#				f.write(audio.get_wav_data())
	except sr.UnknownValueError:
		print('unknown value error')
	except sr.RequestError as e:
		print('failed'.format(e))
	except sr.WaitTimeoutError:
		print('nothing heard before the timeout')

def getDists(ColorToSend = -1):
	
	dataRec = conn.recv(4096).decode()
	distances = dataRec.split(',') #1st elem is p1 dist and 2nd is p2 dist
	#print(dataRec)
	#print(distances)
	if( ColorToSend != -1):
		conn.send(str(ColorToSend).encode()) 
	return distances
		
def checkDists(p1, p2):
	distances = getDists();
	if (abs(float(distances[0]) - p1) > 12):
		print("Player 1 moving while light is red!")
		print("Player 1 go back to the beginning")
		time.sleep(5)
	##add functionality to check when return to beginning?
	
	
	if (abs(float(distances[1]) - p2) > 12):
		print("Player 2 moving while light is red!")
		print("Player 2 go back to the beginning")
		time.sleep(5)
				
def getRandTime():
	return random.uniform(RAND_LOW, RAND_HIGH)

if __name__ == "__main__": 
	#print "Executed when invoked directly"
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Assigns a port for the server that listens to clients connecting to this port.
	serv.bind(('', 808)) #192.168.43.65 #0.0.0.0.0
	serv.listen(5)
	conn, addr = serv.accept() ##not sure about positioning - in or out of loop
	try:
		
		
#		ColorToSend = RED
		getDists(RED)
		
		#print(distances)
			
		#while (abs(distances[0]-distances[1]) >  12):
		#	print("Players please arrange yourselves to be equidistant from the screen")
		#	time.sleep(1)
		#	getDists()
			
		while 1:  #alternating red and green and printing dist data
			distances = getDists(GREEN)
			print(distances)
#			time.sleep(getRandTime())
			distances = getDists(RED)
			print(distances)
#			time.sleep(getRandTime()) 
			
			#getDists()
			#print(distances)
			#if(len(distances) == 2):
			#	print("enter if")
			#	checkDists(float(distances[0]), float(distances[1]))
			#print("P1: %d \tP2: %d" % (distances[0], distances[1]))
			



	except KeyboardInterrupt:
		print("\nKeyboard Interrupt!\nCleaning up\n")
	except ConnectionAbortedError:
		print("Connection Aborted by Client")
	except ConnectionResetError:
		print("Connection Reset by Client")
	finally:
		conn.close()
	
#	changeLight(RED)
#	while 1:
		#change light red to green and back and measure dist of players
#		startPlayer1Dist = getDists(1)
#		startPlayer2Dist = getDists(2)



#else: 
	#print "Executed when imported"
