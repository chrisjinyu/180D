from playsound import playsound
import speech_recognition as sr
import socket
import sys
import random
import time
import Listen


WRONG_ANSWER = "files/buzzer.wav"
CORRECT_ANSWER = "files/clang.mp3"
GAME_WIN = "files/TaDa.mp3"

#P1MIC_INDEX = 1 ##calibrate for computer !!!
#P2MIC_INDEX = 2 

RAND_LOW = 1
RAND_HIGH = 2
FORGIVE_TIME = 0.25 #time after light goes red to forgive movement
FORGIVE_DIST = 4 #inches players can move when not allowed to move without penalty
WIN_DIST = 12 #inches away from ultrasonic sensors that is considered the finish line

RED = 0#.encode() #red light output
GREEN = 1#.encode() # green light output
WARNING = 2#.encode() #warning for when getting close to moving too much
FAULT = 3#.encode() #when player has moved too much and must go back


#Questions = {
#1: "True or False:\nAbraham Lincoln was the first president of the United States.",
#2: "True or False:\n4+4 equals 8",
#3: "How many protons are in a gold atom?\nChoose one of the following options:\nAlpha: 64\t Beta: 69\t Charlie: 79\t Delta: 84"
#}
#Answers = { # store as strings?
#1: "false",
#2: "true",
#3: "charlie"
#}

Questions = {
1: "When driving in fog, you should use your:\nAlpha:Fog lights only\t Beta:High beams\t Charlie:Low beams"
2: "You just sold your vehicle. You must notify the DMV within how many days?\nAlpha:5\t Beta:10\t Charlie:15"
3: "True or False:\nTo avoid last minute moves, you should be looking down the road to where your vehicle will be in about 5 to 10 seconds."
4: "You have been involved in a minor traffic collision with a parked vehicle and you can't find the owner. You must:\nAlpha: Leave a note on the vehicle\t Beta: Report accident without delay to city police or CHP\t Charlie: Both \t Delta: neither"
5: "Unless otherwise posted the speed limit in a residential area is:\nAlpha: 15mph\t Beta: 25mph\t Charlie: 35mph"
6: "To turn left from a multilane one-way street into a one-way street, you should start your turn from: \nAlpha: Any lane(as long as it is safe)\t Beta: The lane closest to the left curb\t Charlie: The lane in the center of the road"
7: "You may not park your vehicle:\nAlpha: On the side of the freeway in an emergency\t Beta: Next to a red painted curb\t Charlie: Within 100 feet of an elementary school"
8: "Two sets of solid, double, yellow lines that are two or more feet apart:\nAlpha: May be crossed to enter or exit a private driveway\t Beta: May not be crossed for any reason\t Charlie: Should be treated as a seperate traffic lane"
9: "It is illegal to park your vehicle:\nAlpha: In an unmarked crosswalk\t Beta: Within three feet of a private driveway\t Charlie: In a bicycle lane"
10: "A solid yellow line next to a broken yellow line means that vehicles:\nAlpha: in both directions may pass\t Beta: Next to a broken line may pass\t Charlie: Next to the solid line may pass"
}

Answers={
1:"charlie"
2:"alpha"
3:"false"
4:"charlie"
5:"Beta"
6:"Beta"
7:"Beta"
8:"Beta"
9:"Alpha"
10:"Beta"
}





def recogGesture():
	return True

def chooseQuestion():
	num = random.randrange(1, len(Questions)+1)
	return (Questions[num], num)

def listen(playerNum):
	return Listen.listen(playerNum)

def getDists(ColorToSend = -1):
	conn.send(str(ColorToSend).encode()) 
	dataRec = conn.recv(4096).decode()
	distances = dataRec.split(',') #1st elem is p1 dist and 2nd is p2 dist
	return distances

def moveBackToStart(playerNum):
	global initDists
	playerIndex = playerNum - 1
	distances = getDists()
	gap = float(initDists[playerIndex])-float(distances[playerIndex])
	print("gap: " + str(gap)) 
	while( gap > FORGIVE_DIST):
		print("Player %d move back to the start line!" % (playerNum))
		print("You still have %d inches to go" % (gap - FORGIVE_DIST))
		time.sleep(3)
		distances = getDists()
		gap = float(initDists[playerIndex])-float(distances[playerIndex])
	print("Resuming play shortly...")
	time.sleep(2)
		
def checkDists(currDists): # , initDists):  #curr is where they should be and init is where they have to return to if they have moved > 1ft from curr
	p1 = float(currDists[0])
	p2 = float(currDists[1])
	distances = getDists(RED)
	print("init dists: %f & %f" % (p1, p2)) 
	print("new dists: %f & %f" % (float(distances[0]), float(distances[1]))) 
	print("diff dists: %f & %f" % (abs(float(distances[0]) - p1), abs(float(distances[1]) - p2)))
	
	if (abs(float(distances[0]) - p1) > FORGIVE_DIST):
		print("Player 1 moving while light is red!")
		print("Player 1 go back to the beginning")
		moveBackToStart(1)
		
	
	##add functionality to check when return to beginning?
	
	if (abs(float(distances[1]) - p2) > FORGIVE_DIST):
		print("Player 2 moving while light is red!")
		print("Player 2 go back to the beginning")
		moveBackToStart(2)
				
def getRandTime():
	return random.uniform(RAND_LOW, RAND_HIGH)

def administerQuestion(playerNum): #playerNum is 1 or 2
	QnA = chooseQuestion() #QnA is a tuple of the question and the question number
	print(QnA[0])
	audio = listen(playerNum)
	while (audio == "null"):
		print("Error, Try again")
		audio = listen(playerNum)
	
	#if Answers[QnA[1]] == "true":
		
	print(audio)
	
	if Answers[QnA[1]] in audio.lower():
		print ("answer correct!")
		playsound(CORRECT_ANSWER)
		return True
	else: ##add ability to relisten when audio deciphered but doesn't contain  
		print("answer incorrect!")
		playsound(WRONG_ANSWER)
		return False

def checkAndAdminGesture(playerNum):
	distances = getDists()
	playerIndex = playerNum - 1
	if float(distances[playerIndex]) < WIN_DIST:
			print("Player %d move to the center area and get ready to perform a gesture" % (playerNum))
			time.sleep(5)
			if recogGesture():
				print("\nCongratulations Player %d! You win!\n" % (playerNum))
				playsound(TaDa)
				time.sleep(5)
				sys.exit()
			else:
				print("Gesture recognition failed. Return to the start line")
				moveBackToStart(playerNum)
	
if __name__ == "_main__": 
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.bind(('', 808)) #192.168.43.65 #0.0.0.0.0
	serv.listen(5)
	conn, addr = serv.accept() ##not sure about positioning - in or out of loop
	
	try:
		while 1:
			distances = getDists(RED)
			print("p1: " + str(distances[0]) + "    p2: " + str(distances[1]))
	except KeyboardInterrupt:
		print("\nKeyboard Interrupt!\nCleaning up\n")
	except ConnectionAbortedError:
		print("Connection Aborted by Client")
	except ConnectionResetError:
		print("Connection Reset by Client")
	finally:
		conn.close()
		
		
		
if __name__ == "__main__": 
	if (len(Questions) != len(Answers)):
		print("error! length of questions must equal length of answers\nExiting...")
		exit()
	
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.bind(('', 808)) #192.168.43.65 #0.0.0.0.0
	serv.listen(5)
	conn, addr = serv.accept() ##not sure about positioning - in or out of loop
	
	try:
		getDists(RED)
		
		##wait for distances to not be zero ??
		
		distances = getDists()
		while( float(distances[0]) == 0 or float(distances[1]) == 0):
			distances = getDists()
		
		print("Players please arrange yourselves to be equidistant from the screen")
		while (abs(float(distances[0])-float(distances[1])) >  FORGIVE_DIST):
			print("Players please arrange yourselves to be equidistant from the screen")
			time.sleep(1)
			distances = getDists()
		initDists = getDists()  ## move location of init dists?

		print("Game beginning soon...")
		time.sleep(1)
		print("Move forward when the light is green and stop when it is red")
		time.sleep(1)
		print("If you move when the light is red, you must start over!")
		time.sleep(1)
		print("At red lights, there will be trivia question which player 1 and 2 will take turns to answer")
		time.sleep(1)
		print("Upong reaching the finish line, players must perform a certain pose to claim victory")
		time.sleep(1)
		print("\nGet ready, game beginning soon...")
		time.sleep(4)
		
		
		#listen(1)
		#listen(2)
		
		while 1:  #main game loop
#			ColorToSend(GREEN)
			getDists(GREEN)
			time.sleep(getRandTime())
			getDists(RED)
			time.sleep(FORGIVE_TIME) 
			redDists = getDists(RED)
			checkAndAdminGesture(1)
			checkAndAdminGesture(2)
			checkDists(redDists)
			#time.sleep(getRandTime())
			administerQuestion(1)
			checkDists(redDists)
			
			administerQuestion(2)
			
			checkDists(redDists)
			
			
			#getDists()
			#p1Dist = distances[0]
			#p2Dist = distances[1]
			#while 1:
			#	checkDists(p1Dist, p2Dist)
			#	ADMINISTER_QUESTION() ##how to check dist while in question method
			#	checkDists



	except SystemExit:
		print("\nGame over. Cleaning up...\n")
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
'''
		while 1:  #alternating red and green and printing dist data
			distances = getDists(GREEN)
			print(distances)
#			time.sleep(getRandTime())
			distances = getDists(RED)
			print(distances)
#			time.sleep(getRandTime()) 
'''
			
			#getDists()
			#print(distances)
			#if(len(distances) == 2):
			#	print("enter if")
			#	checkDists(float(distances[0]), float(distances[1]))
			#print("P1: %d \tP2: %d" % (distances[0], distances[1]))
			



	
