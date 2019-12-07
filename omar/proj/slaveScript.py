import sys
import time
import bluetooth
import RPi.GPIO as GPIO
SLEEP_TIME = 0.1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.LOW)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,GPIO.LOW)
GPIO.setup(24,GPIO.OUT)
GPIO.output(24,GPIO.LOW)
GPIO.setup(25,GPIO.OUT)
GPIO.output(25,GPIO.LOW)
GPIO.setup(12,GPIO.OUT)
GPIO.output(12,GPIO.LOW)


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
		print('out')

		
		inpString1 = tempParsed[1]
		seq1 = inpString1.split(',')
		timeStep = seq1[len(seq1)-1]
			
		inpString2 = tempParsed[2]
		seq2 = inpString2.split(',')
		
		inpString3 = tempParsed[3]
		seq3 = inpString3.split(',')
		
		inpString4 = tempParsed[4]
		seq4 = inpString4.split(',')
		
		inpString5 = tempParsed[5]
		seq5 = inpString5.split(',')
		


		
		for i in range(len(seq1)-1):
			print("seq[i]:" + str(seq1[i]) + "\ti:" + str(i))
			if seq1[i] == '  ':
				print("led oFF")
				GPIO.output(18, GPIO.LOW)
			else:
				print("led oN")
				GPIO.output(18, GPIO.HIGH)
			
			if seq2[i] == '  ':
				print("led oFF")
				GPIO.output(23, GPIO.LOW)
			else:
				print("led oN")
				GPIO.output(23, GPIO.HIGH)
			
			if seq3[i] == '  ':
				print("led oFF")
				GPIO.output(24, GPIO.LOW)
			else:
				print("led oN")
				GPIO.output(24, GPIO.HIGH)
			
			if seq4[i] == '  ':
				print("led oFF")
				GPIO.output(25, GPIO.LOW)
			else:
				print("led oN")
				GPIO.output(25, GPIO.HIGH)
			
			if seq5[i] == '  ':
				print("led oFF")
				GPIO.output(12, GPIO.LOW)
			else:
				print("led oN")
				GPIO.output(12, GPIO.HIGH)
			
			
			
			time.sleep(float(timeStep))
			

	finally:
		# Clean up the connection
		#        print("Closing current connection")
		connection.close()

	# instantiate reconnection
	#server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

	#port = 1
	#server_sock.bind(("",port))
	#server_sock.listen(1)  

