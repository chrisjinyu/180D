import socket 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.43.8', 8080))
client.send("I AM CLIENT\n".encode())
from_server = client.recv(4096).decode()
client.close()
print(from_server)
