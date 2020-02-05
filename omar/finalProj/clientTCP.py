import socket 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('1.1.1.1', 8080))
client.send("I AM CLIENT\n".encode())
from_server = client.recv(4096).decode()
client.close()
print(from_server)
