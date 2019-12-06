import sys
import time

#must call with 2 args - the path of the sequence file and the time step 
path = str(sys.argv[1])
timeStep = float(sys.argv[2])
#path = 'source.csv'

input = open(path, 'r')
inpString = input.read()
seq = inpString.split(',')
input.close()

for i in range(len(seq)):
	if seq[i] == '1':
		print('1') #, end = " ")
	else:
		print("0") #, end = " ")
	time.sleep(timeStep)

