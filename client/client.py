import sys
import socket
# https://stackoverflow.com/questions/35805078/how-do-i-convert-a-password-into-asterisks-while-it-is-being-entered
# https://www.youtube.com/watch?v=27qfn3Gco00

def str_to_bytes(str):
  return bytes(str, 'utf-8')


def bytes_to_str(data):
  return data.decode('UTF-8')

ip_addr = str(input("Please enter the server ip address you want to connect: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((ip_addr, 5090))
    print('Enter lines of text then Ctrl+D or Ctrl+C to quit')
    while True:
        line = sys.stdin.readline()
        if not line:
            # End of standard input, exit this entire script
            break
        sock.sendall(f'{line}'.encode('utf-8'))
        while True:
            data = sock.recv(128)
            print(data.decode("utf-8"), end='')
            if len(data) < 128:
                # No more of this message, go back to waiting for next message
                break
'''
fromServer = " "
fromUser = ""
while fromServer != "":
    fromServer = bytes_to_str(s.recv(4096))
    print(fromServer)
    if fromServer == "Bye.":
        break
    fromUser = str(input())
    if fromUser != "":
        print("Client: " + fromUser)
        s.send(str_to_bytes(fromUser))
'''




'''
file_name = input(str("Enter the desired filename: "))
file = open(file_name, 'wb')
data = s.recv(2048)
file.write(data)
file.close()
print("File has been received successfully")
'''
