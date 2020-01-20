import gspread
from oauth2client.service_account import ServiceAccountCredentials


data_list = []

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("ECE180D database").sheet1


# Extracts the Names, Bluetooth, and Seating Information
for i in range (2,7):
        data_list.append({"name":str(sheet.cell(i,1).value), "address":str(sheet.cell(i,2).value), "row":str(sheet.cell(i,3).value),"column":str(sheet.cell(i,4).value)})    
        
        
size = len(data_list)

for i in range (0,size):
    name = data_list[i]['name']
    address = data_list[i]['address']
    row = data_list[i]['row']
    col = data_list[i]['column']
    output = name+','+address+','+'('+row+','+col+')'
    print(output)
    
#print(data_list)




