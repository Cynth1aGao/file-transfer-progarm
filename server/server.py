import socket

x = socket.socket()
host = socket.gethostname()
port = 8080
x.bind((host, port))
print("The IP address is: ", socket.gethostbyname(socket.gethostname()))
x.listen(1)
print("Looking for any connections...")
conn, addr = x.accept()
print(addr, "Connected Successfully")

filename = input(str("Please enter the filename of the file: "))
file = open(filename, "rb")
file_data = file.read(1024)
conn.send(file_data)
print("File has been sent successfully")