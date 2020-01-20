Steps to get both devices paired and connected:

1: Pair Raspberry Pi's
note: In a bluetooth connection, we can pair as many devices as we can; however, we 
can only connect to 7 devices at the same time. (in our design, we can assume that
the devices are all paired)

	- in order to pair the devices go ahead and follow the steps in the link below
	Note: to recall in the last lab section that we tried to connect bluetooth, 
	I had problems with bluetoothctl. To fix this issue I installed the newest 
	version of Rasbian and it fixed my problem when running bluetoothctl

	link: https://bluedot.readthedocs.io/en/latest/pairpipi.html
	
	-exit bluetoothctl
		-type quit

2: Note the master(server) and slave's (client) bluetooth MAC address

-on respected server and client go to github and clone the rfcomm-server.py in the server's directory
and clone rfcomm-client.py onto the clients local directory

	-On masters command prompt run hciconfig and record MAC address
	-Copy MAC address and replace with the one in rfcomm-client.py

3: Go ahead and run rfcomm-server.py first, then run rfcomm-client.py
-verify that the connection is established and data is transmitting sockets 
