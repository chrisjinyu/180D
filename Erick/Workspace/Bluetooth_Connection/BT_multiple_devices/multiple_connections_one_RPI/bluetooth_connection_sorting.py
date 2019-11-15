import xlrd
import bluetooth
import time
  

  
MAX_ROWS = 4
MAX_COLS = 7
  
nameAddList = []
nameSeatList = []
combinedData = []

#bluetooth port 
port = 1

# Give the location of the file 
loc = ("/home/pi/Desktop/Workspace/Bluetooth_Connection/working_BT_connection/sample_data.xlsx") 
  
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
                    #Connect to bluetooth device
                    con = 0
                    while con == 0:
                        #attempts to connect at all times with the BT address                  
                        try:                            
                            connection(combinedData[k])                       
                            #time.sleep(1)
                            con = 1
                        except:
                            #dummy variable for now
                            a = 1
                            
                            
def connection(socket_data):
    #grabs data
    name    = socket_data['name']
    row     = socket_data['row']
    col     = socket_data['column']
    bd_addr = socket_data['address']
    
    packet = str(name) + ','+str(bd_addr)+','+'('+str(row)+','+str(col)+')'
    
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))
    print ('connection made with ' +name)
    
    sock.send(packet) 
    
                            
def main():
    rows = sheet.nrows
    
    #gathering of data
    gather_data_one(rows)
    gather_data_two(rows)
    
    size_lists = len(nameSeatList)
    #matches seating by names
    matching(size_lists)
    
    #sorts and connects to bluetooth devices
    sort()

if __name__== "__main__":
  main()
    

            