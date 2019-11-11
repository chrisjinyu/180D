import sys
#import numpy as np

#3X5
WIDTH = 3
LENGTH = 5
charDict = {
'A' : [[0,1,0],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
'B' : [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],
'C' : [[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,1,1]],
'D' : [[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,1,0]],
'E' : [[1,1,1],[1,0,0],[1,1,1],[1,0,0],[1,1,1]],
'F' : [[1,1,1],[1,0,0],[1,1,1],[1,0,0],[1,0,0]],
'G' : [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],
'H' : [[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
'I' : [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[1,1,1]],
'J' : [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[1,1,0]],
'K' : [[1,0,1],[1,1,0],[1,0,0],[1,1,0],[1,0,1]],
'L' : [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1]],
'M' : [[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1]],
'N' : [[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
'O' : [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
'P' : [[1,1,1],[1,0,1],[1,1,1],[1,0,0],[1,0,0]],
'Q' : [[1,1,1],[1,0,1],[1,0,1],[1,1,1],[0,0,1]],
'R' : [[1,1,1],[1,0,1],[1,1,1],[1,1,0],[1,0,1]],
'S' : [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
'T' : [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
'U' : [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
'V' : [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
'W' : [[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,0,1]],
'X' : [[1,0,1],[1,0,1],[0,1,0],[1,0,1],[1,0,1]],
'Y' : [[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0]],
'Z' : [[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,1,1]],

'0' : [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
'1' : [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[1,1,1]],
'2' : [[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,1,1]],
'3' : [[1,1,1],[0,0,1],[1,1,1],[0,0,1],[1,1,1]],
'4' : [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],
'5' : [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
'6' : [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],
'7' : [[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,0,0]],
'8' : [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],
'9' : [[1,1,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]], 

' ' : [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
'\'' : [[0,0,1],[0,1,0],[0,0,0],[0,0,0],[0,0,0]],
'\"' : [[0,1,1],[1,1,0],[0,0,0],[0,0,0],[0,0,0]],
#'!'  : [[0,1,0],[0,1,0],[0,1,0],[0,0,0],[0,1,0]],  #skinny !  
'!'  : [[1,1,1],[1,1,1],[1,1,1],[0,0,0],[1,1,1]],   # fat !
'?'  : [[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,0,0]],
','  : [[0,0,0],[0,0,0],[0,1,0],[0,1,0],[1,0,0]],
'.'  : [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,1,0]]
}
#chars = [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,Zero,One,Two,Three,Four,Five,Six,Seven,Eight,Nine]
#'B' : [[,,],[,,],[,,],[,,],[,,]]

def msgOutputter(Msg):
	Msg = Msg.upper()
	for i in range(LENGTH):
		for char in Msg:
			printLine(charDict[char][i])
			print(" ", end = "")
		print()
	print()

def verticalMsgOutputter(Msg):
	Msg = Msg.upper()
	for char in Msg:
		for i in range(LENGTH):
			printLine(charDict[char][i])
			print()
		print()

def outputMsgToFile(Msg):
	output = open('out.txt', 'w')
	Msg = Msg.upper()
	for char in Msg:
		for i in range(LENGTH):
			#printLine(charDict[char][i])
			for j in range(WIDTH):
				if(charDict[char][i][j]):
					print("1", end = "", file = output)
				else:
					print(" ", end = "", file = output)
			print(file = output)
		print("   ", file = output)
	output.close()

#outputMsgToFile("UCLA 2020!")

def printPixel(Pxl):
	if Pxl:
		print ("1", end = "")
	else:
		print (" ", end = "")

def printLine(line):
	for i in range(WIDTH):
		printPixel(line[i])

#vertivalMmsgOutputter("UCLA")
#msgOutputter("UCLA 2020")


REFRESHRATE = 30 #30 times a second
SPEED = 1 #1 line down per second
def msgSeq(msg, height = 15, width = WIDTH):
	#use height and width to make a window that slides down the 
	#vertical message at speed rate
	#-->produces an array of height * width * iterations
	#samples per pixel = time of msg * speed
	#iterations = 
	file = open(msg, 'r')
	lines = file.readlines()
	file.close()
	
	#checking if window too big
	msg_width = 0 # # of chars in 1st line (all lines should be equiv)
	msg_height = 0 # # of lines in msg
	for line in lines:  #error checking and determing msg dimensions
		t_width = 0
		for char in line:
			t_width += 1
		msg_height += 1
		if msg_height == 1:
			msg_width = t_width - 1 #don't count the newline
		elif t_width - 1 > msg_width:
			print("ERROR!\nAll lines must have the same amt of chars", file = sys.stderr)
			print("Line: " + str(msg_height) + " has " + str(t_width-1) + " chars", file = sys.stderr)
	if msg_width < width:
		print("ERROR!\nWidth of text input smaller than window width", file = sys.stderr)
	#print(msg_height)
	#print(msg_width)

	iterations = msg_height - height  #how many iterations to get through msg
	
	#init height x width list of pixel info
	pxls = [[[0 for a in range(width)]for b in range(height)]for c in range(iterations)]

	#pxls = list(np.zeros((iterations, height, width), dtype=np.int8))
	
	for i in range(iterations):
		setPxlArray(pxls[i], lines, i, height)
		
	#printing for visual confirmation
#	for i in range(iterations):
#		for j in range(height):
#			print(pxls[i][j], end = "")
#		print("====")

	#extracting each pixel's seq data
	for i in range(height):
		for j in range (width):
			name = "Pixel" + str(i) + str(j) + ".csv"
			extractPixelData(pxls, "pxlData/" + name, iterations, i, j)
	
	#print individual pixels to confirmation
	for i in range(iterations):
		for j in range(height):
			for k in range(width):
				input = open("pxlData/Pixel"+str(j)+str(k)+".csv")
				pxl_lines = input.readlines() #all in line[0]
				input.close()
				if pxl_lines[0][2*i] == '1':
					print("1", end = "")
				else:
					print(" ", end = "")
#				print(lines[0][2*i], end = "")
			print()	
		print("=======")	
	
def extractPixelData(pixels, outputFile, iterations, h, w):
	#now extract one pixel's [0][1] full sequence to a file in one line
	output = open(outputFile, 'w')
	for i in range(iterations):
		if pixels[i][h][w] == '1':
#		print(pixels[i][h][w])
			print("1", file = output, end = ",")
		else:
			print("0", file = output, end = ",")
	output.close()


#==============
##IDEA: have window start empty and then slowly move text up 
##rather than start with whole first letter on
#==============


def setPxlArray(array, lines, offset, w_height):
#w_.. is window dimensions and offset is offset from top of file
	for ht in range(w_height):
		array[ht]= lines[ht+offset]


msgSeq("out.txt", 9)


#for ch in charDict:
#	msgOutputter(ch)
#	print("====")

