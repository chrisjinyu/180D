import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("a").sheet1

# Extract and print all of the values
# sheet.cell(row, column).value
for i in range (1,16):
    for j in range (1,4):
        print(sheet.cell(i,j).value)

