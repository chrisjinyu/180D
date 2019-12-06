import bluetooth
import time

bd_addr = "B8:27:EB:CB:B6:98"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

print ('connection made')
i = 1
while 1:
    sock.send("data: " + str(i))
    i = i+1
    time.sleep(1)
    

sock.close()


