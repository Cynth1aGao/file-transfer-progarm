import getpass
import socket

# https://stackoverflow.com/questions/35805078/how-do-i-convert-a-password-into-asterisks-while-it-is-being-entered
# https://www.youtube.com/watch?v=27qfn3Gco00




s = socket.socket()
host = input(str("Please enter the host address of the sender: "))
port = 8080
s.connect((host, port))
print("Connected Successfully")

check_account = str(input("Do you have an account? yes/no: "))
check_account_bytes = bytes(check_account, 'utf-8')
s.send(check_account_bytes)

have_account = s.recv(4096)
have_account_str = have_account.decode('UTF-8')

if have_account_str == "Not have account":
    username = input("Enter the username you want to register for this account: ")
    password = input("Enter the password you want to register for this account: ")
    username_bytes = bytes(username, 'utf-8')
    password_bytes = bytes(password, 'utf-8')
    s.send(username_bytes)
    s.send(password_bytes)
    username = input("username: ")
    password = input("password: ")
    username_bytes = bytes(username, 'utf-8')
    password_bytes = bytes(password, 'utf-8')
    s.send(username_bytes)
    s.send(password_bytes)
if have_account_str == "Have account":
    username = input("username: ")
    password = input("password: ")
    username_bytes = bytes(username, 'utf-8')
    password_bytes = bytes(password, 'utf-8')
    s.send(username_bytes)
    s.send(password_bytes)


file_name = input(str("Enter the desired filename: "))
file = open(file_name, 'wb')
data = s.recv(2048)
file.write(data)
file.close()
print("File has been received successfully")