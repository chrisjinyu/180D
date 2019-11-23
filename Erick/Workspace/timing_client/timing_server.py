import bluetooth
import time
import RPi.GPIO as GPIO
SLEEP_TIME = 0.1

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
		# Receive the data         
		data = connection.recv(1024)
		print(data)
		current = time.time()
		#print(current)
		
		parsed = data.split(',')
		diff = float(parsed[1])
		expected_time = float(parsed[0])
		#print(diff)
		latency = current - diff
		#print(latency)
		
		final = time.time() - latency
		
		while(final < expected_time):
			#print(final)
			#time.sleep(1)
			final = time.time() - latency
			print('out')

		while True:
			print('ON')
			GPIO.output(18, GPIO.HIGH)
			time.sleep(SLEEP_TIME)
			print('OFF')
			GPIO.output(18, GPIO.LOW)
			time.sleep(SLEEP_TIME)

	finally:
		# Clean up the connection
		#        print("Closing current connection")
		connection.close()

	# instantiate reconnection
	#server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

	#port = 1
	#server_sock.bind(("",port))
	#server_sock.listen(1)  


