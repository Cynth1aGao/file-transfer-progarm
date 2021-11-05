import socket

# https://www.delftstack.com/howto/python/get-ip-address-python/
# https://www.youtube.com/watch?v=27qfn3Gco00

x = socket.socket()
host = socket.gethostbyname(socket.gethostname())
port = 8080
x.bind((host, port))
print("The IP address is: ", socket.gethostbyname(socket.gethostname()))
x.listen(1)
print("Looking for any connections...")
conn, addr = x.accept()
print(addr, "Connected Successfully")

file_name = input(str("Please enter the filename of the file: "))
file = open(file_name, "rb")
data = file.read(2048)
conn.send(data)
print("File has been sent successfully")