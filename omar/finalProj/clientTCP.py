import socket 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.8', 808))
client.send("I AM CLIENT TCP\n".encode())
from_server = client.recv(4096).decode()
client.close()
print(from_server)
