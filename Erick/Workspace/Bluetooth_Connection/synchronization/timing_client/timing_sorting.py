import xlrd
import bluetooth
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

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
loc = ("/home/pi/Desktop/timing/sample_data.xlsx") 
  
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
                            
                            
def cycleConnections():
	for i in range(0,len(sortedData)):
		#Connect to bluetooth device
                con = 0
                while con == 0:
                	#attempts to connect at all times with the BT address                  
                	try:  
			#connects to next device depending on button
				connection(sortedData[i])                       
		                con = 1
                        except:
                        	#dummy variable for now
                         	a = 1

def connection(socket_data):
	global latency
	decode = 'a'

	#grabs data
	name    = socket_data['name']
	row     = socket_data['row']
	col     = socket_data['column']
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

	#timing information packet after connection is made
	#print(str(latency))
	packet = decode + ',' +str(execute_time)+','+str(sys_time)+','+str(latency)
	#print (packet)

	sock.sendall(packet)

	#retrieves latency for first connection
	data  = (sock.recv(1024))
	
	latency = float(data)

	sock.close()
    
    
                            
def main():
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
    cycleConnections()

if __name__== "__main__":
  main()
    

            
