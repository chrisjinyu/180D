import sys
import time
import bluetooth
import RPi.GPIO as GPIO
SLEEP_TIME = 0.1

#must call with 2 args - the path of the sequence file and the time step 
#path = str(sys.argv[1])
#seq = sys.argv[1]
#timeStep = float(sys.argv[2])

'''
input = open(path, 'r')
inpString = input.read()
seq = inpString.split(',')
input.close()
'''


	

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.LOW)

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

while 1:	#Wait for a connection
	print('waiting for a connection')
	connection, client_address = server_sock.accept()
	GPIO.output(18,GPIO.HIGH)
	try:
		print('connection made')
		# Receive the data         
		data = (connection.recv(1024))
		print(data)
		current = time.time()
		tempParsed = data.split('--') #tempParsed[0] is ericks and 1 is omar's
		
		
		parsed = tempParsed[0].split(',')
		id = parsed[0]
		diff = float(parsed[2])
		expected_time = float(parsed[1])

		# device is the latency initializer
		if (id == 'i'):
			latency = abs(current - diff)
		# reads initializers latency
		else:
			latency = float(parsed[3])

#		print (latency)
		final = time.time() - latency

		packet = str(latency)
		connection.sendall(packet)
		while(final < expected_time):
			final = time.time() - latency
		#print('out')


		inpString = tempParsed[1]
		seq = inpString.split(',')
		timeStep = seq[len(seq)-1]
				
		for i in range(len(seq)-1):
			if seq[i] == '1':
				GPIO.output(18, GPIO.HIGH)
			else:
				GPIO.output(18, GPIO.LOW)
			time.sleep(timeStep)
			

	finally:
		# Clean up the connection
		#        print("Closing current connection")
		connection.close()

	# instantiate reconnection
	#server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

	#port = 1
	#server_sock.bind(("",port))
	#server_sock.listen(1)  

