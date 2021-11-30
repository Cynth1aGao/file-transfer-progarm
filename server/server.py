import socket
import os
from _thread import *
from file_transfer import file_transfer_protocol

# https://www.delftstack.com/howto/python/get-ip-address-python/
# https://www.youtube.com/watch?v=27qfn3Gco00
def str_to_bytes(str):
  return bytes(str, 'utf-8')

def bytes_to_str(data):
  return data.decode('UTF-8')

global_account_dict = {}
x = socket.socket()
host = socket.gethostbyname(socket.gethostname())
port = 8080
print("The IP address is: ", socket.gethostbyname(socket.gethostname()))


ThreadCount = 0
try:
    x.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
x.listen(5)

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        response = 'Server message: ' + bytes_to_str(data)
        if not data:
            break
        connection.sendall(str.encode(response))
    connection.close()

while True:
    conn, address = x.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (conn, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

x.close()

'''
class filetransfer:
  def __init__(self, socket, global_account_dict):
    self.accounts = global_account_dict

  def create_account(self):
    check_account = conn.recv(4096)
    if check_account.decode('UTF-8') == "yes":
      have_account = "Have account"
      conn.send(bytes(have_account, 'utf-8'))
      self.login()
    elif check_account.decode('UTF-8') == "no":
      have_account = "Not have account"
      conn.send(bytes(have_account, 'utf-8'))
      while True:
        username = conn.recv(4096)
        username_str = username.decode('UTF-8')
        password = conn.recv(4096)
        password_str = password.decode('UTF-8')
        have_username = "Not have username"
        if username_str not in self.accounts:
          conn.send(bytes(have_username, 'utf-8'))
          self.accounts[username_str] = password_str
          self.login()
          break
        else:
          have_username = "Have username"
          conn.send(bytes(have_username, 'utf-8'))
          print("The username you entered already existed, please change to another one")

  def login(self):
    while True:
      username = conn.recv(4096)
      username_str = username.decode('UTF-8')
      password = conn.recv(4096)
      password_str = password.decode('UTF-8')
      if username_str in self.accounts and password_str == self.accounts[username_str]:
        print('Logging on ...')
        print('All done!')
        break
      else:
        print('Incorrect password.')
        print('Try again!')
user1 = file_transfer_protocol(conn, account_dict)
user1.create_account()
'''

file_name = input(str("Please enter the filename of the file: "))
file = open(file_name, "rb")
data_read = file.read(2048)
conn.send(data_read)
print("File has been sent successfully")