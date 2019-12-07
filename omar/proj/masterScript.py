import sys
import time
import xlrd
import bluetooth
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
#import numpy as np

#3X5
WIDTH = 3
LENGTH = 5
charDict35 = {
'A' : [[0,1,0],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
'B' : [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,1,0]],
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
'.'  : [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,1,0]],


'#'  : [[1,0,1],[0,0,0],[0,0,0],[1,0,1],[1,1,1]] #smiley
}

charDict45 = {
'A' : [[0,1,1,0],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1]],
'B' : [[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,0,1],[1,1,1,0]],
'C' : [[1,1,1,1],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,1,1,1]],
'D' : [[1,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,0]],
'E' : [[1,1,1,1],[1,0,0,0],[1,1,1,0],[1,0,0,0],[1,1,1,1]],
'F' : [[1,1,1,1],[1,0,0,0],[1,1,1,1],[1,0,0,0],[1,0,0,0]],
'G' : [[1,1,1,1],[1,0,0,0],[1,0,1,1],[1,0,0,1],[1,1,1,1]],
'H' : [[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1]],
'I' : [[1,1,1,1],[0,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1]],
'J' : [[1,1,1,1],[0,0,1,0],[0,0,1,0],[0,0,1,0],[1,1,1,0]],
'K' : [[1,0,0,1],[1,0,1,0],[1,1,0,0],[1,0,1,0],[1,0,0,1]],
'L' : [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,1,1,1]],
'M' : [[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,0,0,1]],
'N' : [[1,0,0,1],[1,1,0,1],[1,0,0,1],[1,0,1,1],[1,0,0,1]],
'O' : [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]],
'P' : [[1,1,1,1],[1,0,0,1],[1,1,1,1],[1,0,0,0],[1,0,0,0]],
'Q' : [[1,1,1,1],[1,0,0,1],[1,0,1,1],[1,1,1,1],[0,0,1,0]],
'R' : [[1,1,1,1],[1,0,0,1],[1,1,1,1],[1,0,1,0],[1,0,0,1]],
'S' : [[1,1,1,1],[1,0,0,0],[1,1,1,1],[0,0,0,1],[1,1,1,1]],
'T' : [[1,1,1,1],[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0]],
'U' : [[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]],
'V' : [[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0]],
'W' : [[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,0,0,1]],
'X' : [[1,0,0,1],[1,0,0,1],[0,1,1,0],[1,0,0,1],[1,0,0,1]],
'Y' : [[1,0,0,1],[1,0,0,1],[0,1,1,0],[0,1,1,0],[0,1,1,0]],
'Z' : [[1,1,1,1],[0,0,1,0],[0,1,0,0],[1,0,0,0],[1,1,1,1]],

'0' : [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]],
'1' : [[0,0,1,0],[0,1,1,0],[0,0,1,0],[0,0,1,0],[1,1,1,1]],
'2' : [[1,1,1,1],[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,1,1,1]],
'3' : [[1,1,1,1],[0,0,0,1],[1,1,1,1],[0,0,0,1],[1,1,1,1]],
'4' : [[1,0,0,1],[1,0,0,1],[1,1,1,1],[0,0,0,1],[0,0,0,1]],
'5' : [[1,1,1,1],[1,0,0,0],[1,1,1,0],[0,0,0,1],[1,1,1,0]],
'6' : [[1,1,1,1],[1,0,0,0],[1,1,1,1],[1,0,0,1],[1,1,1,1]],
'7' : [[1,1,1,1],[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]],
'8' : [[1,1,1,1],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,1,1,1]],
'9' : [[1,1,1,1],[1,0,0,1],[1,1,1,1],[0,0,0,1],[0,0,0,1]], 

' '  : [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
'\'' : [[0,0,1,0],[0,0,1,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]],
'\"' : [[0,1,0,1],[0,1,0,1],[1,0,1,0],[0,0,0,0],[0,0,0,0]], 
'!'  : [[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,0,0,0],[0,1,1,0]],   
'?'  : [[1,1,1,1],[0,0,0,1],[0,1,1,1],[0,1,0,0],[0,1,0,0]],
','  : [[0,0,0,0],[0,0,0,0],[0,0,1,0],[0,0,1,0],[0,1,0,0]],
'.'  : [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,1,1,0],[0,1,1,0]],

'#'  : [[1,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,1],[0,1,1,0]] #smiley
}
#'B' : [[,,,],[,,,],[,,,],[,,,],[,,,]]

charDict55 = {
'A' : [[0,1,1,1,0],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1]],
'B' : [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0]],
'C' : [[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
'D' : [[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0]],
'E' : [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,1,1,1,1]],
'F' : [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0]],
'G' : [[1,1,1,1,1],[1,0,0,0,0],[1,0,1,1,1],[1,0,0,0,1],[1,1,1,1,1]],
'H' : [[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1]],
'I' : [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
'J' : [[1,1,1,1,1],[0,0,0,1,0],[0,0,0,1,0],[0,1,0,1,0],[0,1,1,1,0]],
'K' : [[1,0,0,1,0],[1,0,1,0,0],[1,1,0,0,0],[1,0,1,0,0],[1,0,0,1,0]],
'L' : [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
'M' : [[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1]],
'N' : [[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1]],
'O' : [[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]],
'P' : [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0]],
'Q' : [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,1,1,1,1],[0,0,0,1,0]],
'R' : [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,1,0,0],[1,0,0,1,0]],
'S' : [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,1],[0,0,0,0,1],[1,1,1,1,1]],
'T' : [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
'U' : [[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]],
'V' : [[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0]],
'W' : [[1,0,0,0,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,1,0,1],[1,1,1,1,1]],
'X' : [[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]],
'Y' : [[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0],[0,0,1,0,0],[0,0,1,0,0]],
'Z' : [[1,1,1,1,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,1,1,1,1]],

'0' : [[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]],
'1' : [[0,0,1,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
'2' : [[1,1,1,1,1],[0,0,0,0,1],[0,0,0,1,0],[0,1,1,0,0],[1,1,1,1,1]],
'3' : [[1,1,1,1,0],[0,0,0,0,1],[1,1,1,1,0],[0,0,0,0,1],[1,1,1,1,0]],
'4' : [[1,0,0,1,0],[1,0,0,1,0],[1,1,1,1,1],[0,0,0,1,0],[0,0,0,1,0]],
'5' : [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[0,0,0,0,1],[1,1,1,1,0]],
'6' : [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1]],
'7' : [[1,1,1,1,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,0,0,0,0]],
'8' : [[0,1,1,1,0],[1,0,0,0,1],[0,1,1,1,0],[1,0,0,0,1],[0,1,1,1,0]],
'9' : [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1],[0,0,0,0,1],[0,0,0,0,1]], 

' '  : [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
'\'' : [[0,0,1,0,0],[0,0,1,0,0],[0,1,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
'\"' : [[0,1,0,0,1],[0,1,0,0,1],[1,0,0,1,0],[0,0,0,0,0],[0,0,0,0,0]], 
'!'  : [[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,1,0,0]],   
'?'  : [[0,1,1,1,0],[1,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,0,1,0,0]],
','  : [[0,0,0,0,0],[0,0,1,1,0],[0,0,1,1,0],[0,0,0,1,0],[0,1,1,0,0]],
'.'  : [[0,0,0,0,0],[0,0,0,0,0],[1,1,1,0,0],[1,1,1,0,0],[1,1,1,0,0]],


'~'  : [[0,1,0,1,0],[1,0,1,0,1],[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0]], 	#heart
'#'  : [[0,1,0,1,0],[0,0,0,0,0],[0,0,1,0,0],[1,0,0,0,1],[0,1,1,1,0]] 	#smiley
}

charDict65 = {
'A' : [[0,1,1,1,1,0],[1,0,0,0,0,1],[1,1,1,1,1,1],[1,0,0,0,0,1],[1,0,0,0,0,1]],
'B' : [[1,1,1,1,1,0],[1,0,0,0,0,1],[1,1,1,1,1,0],[1,0,0,0,0,1],[1,1,1,1,1,0]],
'C' : [[0,1,1,1,1,1],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[0,1,1,1,1,1]],
'D' : [[1,1,1,1,1,0],[1,0,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,1],[1,1,1,1,1,0]],
'E' : [[1,1,1,1,1,1],[1,0,0,0,0,0],[1,1,1,1,1,0],[1,0,0,0,0,0],[1,1,1,1,1,1]],
'F' : [[1,1,1,1,1,1],[1,0,0,0,0,0],[1,1,1,1,1,0],[1,0,0,0,0,0],[1,0,0,0,0,0]],
'G' : [[1,1,1,1,1,1],[1,0,0,0,0,0],[1,0,0,1,1,1],[1,0,0,0,0,1],[1,1,1,1,1,1]],
'H' : [[1,0,0,0,0,1],[1,0,0,0,0,1],[1,1,1,1,1,1],[1,0,0,0,0,1],[1,0,0,0,0,1]],
'I' : [[1,1,1,1,1,1],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[1,1,1,1,1,1]],
'J' : [[1,1,1,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[1,0,0,1,0,0],[1,1,1,1,0,0]],
'K' : [[1,0,0,0,1,1],[1,0,0,1,0,0],[1,1,1,0,0,0],[1,0,0,1,0,0],[1,0,0,0,1,1]],
'L' : [[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,1,1,1,1,1]],
'M' : [[1,0,0,0,0,1],[1,1,0,0,1,1],[1,0,1,1,0,1],[1,0,0,0,0,1],[1,0,0,0,0,1]],
'N' : [[1,1,0,0,0,1],[1,0,1,0,0,1],[1,0,0,1,0,1],[1,0,0,0,1,1],[1,0,0,0,0,1]],
'O' : [[0,1,1,1,1,0],[1,0,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,1],[0,1,1,1,1,0]],
'P' : [[1,1,1,1,1,1],[1,0,0,0,0,1],[1,1,1,1,1,1],[1,0,0,0,0,0],[1,0,0,0,0,0]],
'Q' : [[1,1,1,1,1,1],[1,0,0,0,0,1],[1,0,0,1,0,1],[1,1,1,1,1,1],[0,0,0,1,0,0]],
'R' : [[1,1,1,1,1,0],[1,0,0,0,0,1],[1,1,1,1,1,0],[1,0,1,0,0,0],[1,0,0,1,1,0]],
'S' : [[0,1,1,1,1,1],[1,0,0,0,0,0],[0,1,1,1,1,0],[0,0,0,0,0,1],[0,1,1,1,1,0]],
'T' : [[1,1,1,1,1,1],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0]],
'U' : [[1,0,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,1],[0,1,1,1,1,0]],
'V' : [[1,0,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,1],[0,1,0,0,1,0],[0,0,1,1,0,0]],
'W' : [[1,0,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,1],[1,0,1,1,0,1],[0,1,0,0,1,0]],
'X' : [[1,0,0,0,0,1],[0,1,0,0,1,0],[0,0,1,1,0,0],[0,1,0,0,1,0],[1,0,0,0,0,1]],
'Y' : [[1,0,0,0,0,1],[1,0,0,0,0,1],[0,1,1,1,1,0],[0,0,1,1,0,0],[0,0,1,1,0,0]],
'Z' : [[1,1,1,1,1,1],[0,0,0,1,1,0],[0,0,1,1,0,0],[0,1,1,0,0,0],[1,1,1,1,1,1]],

'0' : [[0,1,1,1,1,0],[1,0,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,1],[0,1,1,1,1,0]],
'1' : [[0,0,1,1,0,0],[0,1,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[1,1,1,1,1,1]],
'2' : [[0,1,1,1,1,1],[1,0,0,0,0,1],[0,0,1,1,1,0],[0,1,0,0,0,0],[1,1,1,1,1,1]],
'3' : [[1,1,1,1,1,0],[0,0,0,0,0,1],[0,1,1,1,1,0],[0,0,0,0,0,1],[1,1,1,1,1,0]],
'4' : [[1,0,0,0,1,0],[1,0,0,0,1,0],[1,1,1,1,1,1],[0,0,0,0,1,0],[0,0,0,0,1,0]],
'5' : [[1,1,1,1,1,1],[1,0,0,0,0,0],[1,1,1,1,1,0],[0,0,0,0,0,1],[1,1,1,1,1,0]],
'6' : [[1,1,1,1,1,1],[1,0,0,0,0,0],[1,1,1,1,1,1],[1,0,0,0,0,1],[1,1,1,1,1,1]],
'7' : [[1,1,1,1,1,1],[0,0,0,0,1,0],[0,0,0,1,0,0],[0,0,1,0,0,0],[0,1,0,0,0,0]],
'8' : [[0,1,1,1,1,0],[1,0,0,0,0,1],[0,1,1,1,1,0],[1,0,0,0,0,1],[0,1,1,1,1,0]],
'9' : [[1,1,1,1,1,1],[1,0,0,0,0,1],[1,1,1,1,1,1],[0,0,0,0,0,1],[0,0,0,0,0,1]], 

' '  : [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],
'\'' : [[0,0,1,0,0,0],[0,0,1,0,0,0],[0,1,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],
'\"' : [[0,0,1,0,0,1],[0,0,1,0,0,1],[0,1,0,0,1,0],[0,0,0,0,0,0],[0,0,0,0,0,0]], 
'!'  : [[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,0,0,0,0],[0,0,1,1,0,0]],   
'?'  : [[1,1,1,1,1,1],[1,0,0,0,0,1],[0,0,1,1,1,1],[0,0,1,0,0,0],[0,0,1,0,0,0]],
','  : [[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,0,1,0,0],[0,0,1,0,0,0],[0,1,0,0,0,0]],
'.'  : [[0,0,0,0,0,0],[0,1,1,1,0,0],[0,1,1,1,0,0],[0,1,1,1,0,0],[0,0,0,0,0,0]],


'~'  : [[1,1,0,0,1,1],[1,0,1,1,0,1],[1,0,0,0,0,1],[0,1,0,0,1,0],[0,0,1,1,0,0]], 	#heart
'#'  : [[1,1,0,0,1,1],[0,0,0,0,0,0],[0,0,1,1,0,0],[1,0,0,0,0,1],[0,1,1,1,1,0]] 	#smiley
}

charDict56 = {
'A' : [[0,1,1,1,0],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]],
'B' : [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0]],
'C' : [[0,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
'D' : [[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0]],
'E' : [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
'F' : [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]],
'G' : [[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,0,1,1,1],[1,0,0,0,1],[1,1,1,1,1]],
'H' : [[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]],
'I' : [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
'J' : [[1,1,1,1,1],[0,0,0,1,0],[0,0,0,1,0],[0,1,0,1,0],[0,1,0,1,0],[0,1,1,1,0]],
'K' : [[1,0,0,0,1],[1,0,0,1,0],[1,1,1,0,0],[1,1,1,0,0],[1,0,0,1,0],[1,0,0,0,1]],
'L' : [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
'M' : [[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]],
'N' : [[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1]],
'O' : [[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]],
'P' : [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]],
'Q' : [[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,1,0,1],[1,1,1,1,1],[0,0,0,1,0]],
'R' : [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,1,0,0],[1,0,0,1,0],[1,0,0,0,1]],
'S' : [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,1],[0,0,0,0,1],[0,0,0,0,1],[1,1,1,1,1]],
'T' : [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
'U' : [[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]],
'V' : [[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0]],
'W' : [[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,1,0,1],[1,1,0,1,1],[1,0,0,0,1]],
'X' : [[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1],[1,0,0,0,1]],
'Y' : [[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
'Z' : [[1,1,1,1,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],

'0' : [[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]],
'1' : [[0,1,1,0,0],[1,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
'2' : [[0,1,1,1,0],[1,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,1,1,1,1]],
'3' : [[1,1,1,1,0],[0,0,0,0,1],[1,1,1,1,0],[0,0,0,0,1],[0,0,0,0,1],[1,1,1,1,0]],
'4' : [[1,0,0,1,0],[1,0,0,1,0],[1,1,1,1,1],[0,0,0,1,0],[0,0,0,1,0],[0,0,0,1,0]],
'5' : [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[0,0,0,0,1],[0,0,0,0,1],[1,1,1,1,0]],
'6' : [[0,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1]],
'7' : [[1,1,1,1,1],[0,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,0,0,0,0]],
'8' : [[0,1,1,1,0],[1,0,0,0,1],[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
'9' : [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1],[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1]], 

' '  : [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
'\'' : [[0,0,1,0,0],[0,0,1,0,0],[0,1,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
'\"' : [[0,1,0,0,1],[0,1,0,0,1],[1,0,0,1,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]], 
'!'  : [[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0],[0,0,0,0,0],[0,1,1,1,0]],   
'?'  : [[0,1,1,1,0],[1,0,0,0,1],[0,0,1,1,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
','  : [[0,0,0,0,0],[0,0,0,0,0],[0,1,1,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,1,0,0,0]],
'.'  : [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0]],


'~'  : [[0,1,0,1,0],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0]], 	#heart
'#'  : [[0,1,0,1,0],[0,0,0,0,0],[0,0,1,0,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]] 	#smiley
}



charDicts = { 35: charDict35, 
			  45: charDict45, 
			  55: charDict55, 
			  65: charDict65,
			  56: charDict56}

#chars = [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,Zero,One,Two,Three,Four,Five,Six,Seven,Eight,Nine]
#'B' : [[,,],[,,],[,,],[,,],[,,]]

def msgOutputter(Msg, dict = charDict35, width = WIDTH, length = LENGTH):
	Msg = Msg.upper()
	for i in range(length):
		for char in Msg:
			printLine(dict[char][i], width)
			print " ",
		print()
	print()

def verticalMsgOutputter(Msg, dict = charDict35, width = WIDTH):
	Msg = Msg.upper()
	for char in Msg:
		for i in range(LENGTH):
			printLine(dict[char][i], width)
			print()
		print()

def outputMsgToFile(Msg, w_height, width = WIDTH, dict = charDict35, path = 'out.txt'):
	#w_height is the height of the window for the pre/post rolling
	output = open(path, 'w')
	Msg = Msg.upper()
	for i in range(w_height):
		print >>output, ' ' * width,
				
		#print(' ' * width, file = output)
	for char in Msg:
		for i in range(LENGTH):
			#printLine(charDict[char][i])
			for j in range(width):
				if(dict[char][i][j]):
					print >>output, "1",
					
					#print("1", end = "", file = output)
				else:
					print >>output, "0",
				
#					print(" ", end = "", file = output)
			print >>output, ""
				
			#print(file = output)
		print >>output, " " * width
			
		#print(' ' * width, file = output)
	for i in range(w_height):
		#print(' ' * width, file = output)
		print >>output, " " * width,
			
	output.close()

def outputMsgToFileHorizontally(Msg, w_width, dict = charDict55, height = 5, path = 'out.txt'):
	#w_width is the width of the window used for the pre/post rolling
	output = open(path, 'w')
	Msg = Msg.upper()
	numChar = 0
	for char in Msg:
		numChar += 1
	#print (numChar)
	msgPixelWidth = numChar * 6
	for i in range(height): #for each row of out.txt
		print >>output, " " * width,
#		print(' ' * w_width, end = "", file = output)
		for char in Msg:
			for j in range(5): #for each pixel in a char
				if(dict[char][i][j]):
					print >>output, "1",
			
					#print("1", end = "", file = output)
				else:
					print >>output, " ",
			
					#print(" ", end = "", file = output)
			print >>output, " ",
			
			#print(' ', end = "", file = output)
		print >>output, " " * width
			
		#print(' ' * w_width, file = output)
	output.close()

def printPixel(Pxl):
	if Pxl:
		print "1",
			
#		print ("1", end = "")
	else:
		print " ",

def printLine(line, width = WIDTH):
	for i in range(width):
		printPixel(line[i])

def setPxlArray(array, lines, offset, w_height):
#w_.. is window dimensions and offset is offset from top of file
	for ht in range(w_height):
		array[ht]= lines[ht+offset]

def extractPixelData(pixels, outputFile, iterations, h, w):
	#now extract one pixel's [0][1] full sequence to a file in one line
	output = open(outputFile, 'w')
	for i in range(iterations):
		if pixels[i][h][w] == '1':
#		print(pixels[i][h][w])
			print >>output, "1",
			
#			print("1", file = output, end = ",")
		else:
			print >>output, " ",
			
#			print("0", file = output, end = ",")
	output.close()

def msgSeq(msgPath, width = WIDTH, height = 15, sleepAmt = 0):
	#use height and width to make a window that slides down the 
	#vertical message at speed rate
	#-->produces an array of height * width * iterations
	#samples per pixel = time of msg * speed
	#iterations = 
	file = open(msgPath, 'r')
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
			print >>sys.stderr, "ERROR!\nAll lines must have the same amt of chars"
			print >>sys.stderr, "Line: " + str(msg_height) + " has " + str(t_width-1) + " chars"
				
			#print("ERROR!\nAll lines must have the same amt of chars", file = sys.stderr)
			#print("Line: " + str(msg_height) + " has " + str(t_width-1) + " chars", file = sys.stderr)
	if msg_width < width:
		print >>sys.stderr, "ERROR!\nWidth of text input smaller than window width"
		#print("ERROR!\nWidth of text input smaller than window width", file = sys.stderr)

	iterations = msg_height - height  #how many iterations to get through msg
	
	#init height x width list of pixel info
	pxls = [[[0 for a in range(width)]for b in range(height)]for c in range(iterations)]

	for i in range(iterations):
		setPxlArray(pxls[i], lines, i, height)
		
	#extracting each pixel's seq data
	for i in range(height):
		for j in range (width):
			name = "Pixel" + str(i) + "-" + str(j) + ".csv"
			extractPixelData(pxls, "pxlData/" + name, iterations, i, j)
	
	#print individual pixels to confirmation
	for i in range(iterations):
		for j in range(height):
			for k in range(width):
				input = open("pxlData/Pixel" + str(j) + "-" + str(k)+ ".csv")
				pxl_lines = input.readlines() #all in line[0]
				input.close()
				if pxl_lines[0][2*i] == '1':
					print "1",
					#print("1", end = "")
				else:
					print " ",
					#print(" ", end = "")
			print()	
		print("=" * width)
		time.sleep(sleepAmt)

def msgSeqHorizontal(msgPath, window_width = 15, char_height = 5, sleepAmt = 0):
	#use height and width to make a window that slides across the 
	#horizonatal message
	#-->produces an array of height * width * iterations
	file = open(msgPath, 'r')
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
			print >>sys.stderr, "ERROR!\nAll lines must have the same amt of chars"
			print >>sys.stderr, "Line: " + str(msg_height) + " has " + str(t_width-1) + " chars"
			
			#print("ERROR!\nAll lines must have the same amt of chars", file = sys.stderr)
			#print("Line: " + str(msg_height) + " has " + str(t_width-1) + " chars", file = sys.stderr)
	if msg_width < window_width:
		print >>sys.stderr, "ERROR!\nWidth of text input smaller than window width"
		
		#print("ERROR!\nWidth of text input smaller than window width", file = sys.stderr)
	
	iterations = msg_width - window_width  #how many iterations to get through msg
	
	#init height x width list of pixel info
	pxls = [[[0 for a in range(window_width)]for b in range(char_height)]for c in range(iterations)]

	for i in range(iterations): #i is offset from left
		for c_h in range(char_height):
			for ww in range(window_width):
				pxls[i][c_h][ww] = str(lines[c_h][i+ww])

	#extracting each pixel's seq data
	for i in range(char_height):
		for j in range (window_width):
			name = "Pixel" + str(i) + "-" + str(j) + ".csv"
			extractPixelData(pxls, "pxlData/" + name, iterations, i, j)
	
	#print individual pixelsfor confirmation
	for i in range(iterations):
		for j in range(char_height):
			for k in range(window_width):
				input = open("pxlData/Pixel"+str(j)+"-"+str(k)+".csv")
				pxl_lines = input.readlines() #all in line[0]
				input.close()
				if pxl_lines[0][2*i] == '1':
					print "1",
#					print("1", end = "")
				else:
					print " ",
#					print(" ", end = "")
			print()	
		print("=" * window_width)	
		time.sleep(sleepAmt)

def omarMain(msg, dimension1, dimension2, sleepAmount = 0, HorizontalIfPossible = 1, path = 'out.txt'):
	#first decide which charDict is best
	if dimension1 > dimension2:
		length = dimension1
		width = dimension2
	else:
		length = dimension2
		width = dimension1
	#length = max(dimension1, dimension2)
	#width = min(dimension1, dimension2)
	

	##CAREFUL WTTH LENGTH/WIDTH/HEIGHT IN AND OUT OF DIFFERENT FUNCTIONS
	
	if(HorizontalIfPossible):
		if(width == 5 or width == 6):		# or width == 6):
			outputMsgToFileHorizontally(msg, length, charDicts[int('5'+str(width))], width, path)
			msgSeqHorizontal(path, length, width, sleepAmount)
			return
	if(width == 3 or width == 4 or width == 5 or width == 6):
		outputMsgToFile(msg, length, width, charDicts[int(str(width)+'5')], path)
		msgSeq(path, width, length, sleepAmount)
	else:
		print("ERROR! This width is not supported")


#msg = "the quick brown fox jumped over the lazy dog 1234567890"
msg = "UCLA!"
win_width = 12
time_delay = 0.05

#outputMsgToFileHorizontally("UCLA", 12, charDict56)

#omarMain(msg, 6, win_width, time_delay)
#omarMain(msg, 5, win_width, time_delay)

#omarMain(msg, 6, win_width, time_delay, 0)
#omarMain(msg, 5, win_width, time_delay, 0)
#omarMain(msg, 4, win_width, time_delay)
#omarMain(msg, 3, win_width, time_delay)

'''
for i in range(3,6):
	outputMsgToFile("UCLA", 12,charDicts[i], i)
	msgSeq("out.txt", 12, i)
'''
'''
for ch in charDict35:
	msgOutputter(ch, charDict35, 3)
	print()
	msgOutputter(ch, charDict45, 4)
	print()
	msgOutputter(ch, charDict55, 5)
	print()
	msgOutputter(ch, charDict65, 6)
	print()
	msgOutputter(ch, charDict56, 5, 6)
	print("=========")

msgOutputter('I ~ U', charDict55, 5)
print()
msgOutputter('I ~ U', charDict65, 6)
print()
msgOutputter('I ~ U', charDict56, 5, 6)
print("=========")
'''


# connection button
button = 10
  

# button initialization
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

#time to execute algorithm
min = .30
execute_time = time.time() + 60*min

  
MAX_ROWS = 4
MAX_COLS = 2
  

latency = 1.0

nameAddList = []
nameSeatList = []
combinedData = []
sortedData = []

#bluetooth port 
port = 1

# Give the location of the file 
loc = ("/home/pi/Desktop/180D/180D/Erick/Workspace/Bluetooth_Connection/synchronization/timing_client/test_data.xlsx") 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0)
  
# Gathers name and bluetooth information
def gather_data_one(rows):
	for i in range (1, rows):
		nameAddList.append({"name":sheet.cell_value(i, 0), "address":sheet.cell_value(i, 1)})

# Gathers names and seating location
def gather_data_two(rows):
	for i in range (1, rows):
		nameSeatList.append({"name":sheet.cell_value(i, 4), "row":sheet.cell_value(i, 5), "column":sheet.cell_value(i, 6)})  

# match names with seating
def matching(size_lists):
	for i in range (0,size_lists):
		for j in range (0, size_lists):
			if nameAddList[i]['name'] == nameSeatList[j]['name']:
				combinedData.append({"name":nameAddList[i]['name'], "address":nameAddList[i]['address'], "row":nameSeatList[j]['row'], "column":nameSeatList[j]['column']})
		
# connects and disconnects transmitting name
def sort():
	
	#cycles through the rows and columns, connects, and transmits name
	# note:rows and cols are 1's based 
	for i in range(0, 1):
		for j in range(0, MAX_COLS):
			for k in range (0, MAX_COLS):
				if (int(combinedData[k]['row']) == i+1) and (int(combinedData[k]['column'])==j+1):
					sortedData.append({"name":combinedData[k]['name'], "address":combinedData[k]['address'], "row":combinedData[k]['row'], "column":combinedData[k]['column']})
							
def cycleConnections(timeStep):
	for i in range(0,len(sortedData)):
		#Connect to bluetooth device
		con = 0
		while con == 0:  #attempts to connect at all times with the BT address				  
					try:  
			#connects to next device depending on button
						connection(sortedData[i], timeStep)
						con = 1
					except:
							#dummy variable for now
						a = 1

def connection(socket_data, timeStep):
	global latency
	decode = 'a'

	#grabs data
	name	= socket_data['name']
	row	 = socket_data['row']
	col	 = socket_data['column']
	bd_addr = socket_data['address']

	#sets up bluetooth socket
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((bd_addr, port))
	# the first connections latency is used for all
	if (row == 1.0 and col == 1.0):
		decode = 'i'
	#uses the first connections latency for remaining devices
	else:
		decode = 'l'
	sys_time = time.time()
	print ('connection made with ' +name)
	
	fileName = "Pixel" + str(row + 1) + "-" + str(col + 1) + ".csv"
	print("A")
	print(fileName)
	input = open("pxlData/" + fileName)
	print("A")
	
	lines = input.readlines()
	print("A")
	input.close
	print("A")
	outString = lines[0] #gets 1st line of path
	print("A")
	
	# make last element of outString be the timeStep
	outString = outString + str(timeStep)
	
	print(outString)
	#sock.sendall(outString)
	
	
	#timing information packet after connection is made
	#print(str(latency))
	packet = decode + ',' +str(execute_time)+','+str(sys_time)+','+str(latency) + "--" + outString
	#print (packet)

	print(packet)

	sock.sendall(packet)
	
	
	print("sent")
	

	#retrieves latency for first connection
	data  = (sock.recv(1024))
	
	latency = float(data)

	sock.close()
								
def main():
	omarMain("UCLA", 3, 5)
	
	
	rows = sheet.nrows
	#gathering of data
	gather_data_one(rows)
	gather_data_two(rows)
	
	size_lists = len(nameSeatList)
	#matches seating by names
	matching(size_lists)
	
	#sorts seating in increasing order
	sort()

	#connects to paired devices
	cycleConnections(1)

if __name__== "__main__":
  main()
	

			