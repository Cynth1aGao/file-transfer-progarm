import getpass
import socket


class filetransfer:
  def __init__(self):
    self.accounts = {}
  def create_account(self):
    checkaccount = input("Do you have an account? yes/no: ")
    if checkaccount == "yes":
      self.login()
    elif checkaccount == "no":
      while True:
        username = input("Enter the username you want to register for this account: ")
        password = getpass.getpass("Enter the password you want to register for this account: ")
        if username not in self.accounts:
          self.accounts[username] = password
          self.login()
          break
        else:
          print("The username you entered already existed, please change to another one")
  def login(self):
    while True:
      user = input("Username: ")
      pwd = getpass.getpass("Password: ")
      if user in self.accounts and pwd == self.accounts[user]:
        print('Logging on ...')
        print('All done!')
        break
      else:
        print('Incorrect password.')
        print('Try again!')

user1 = filetransfer()
user1.create_account()


s = socket.socket()
host = input(str("Please enter the host address of the sender: "))
port = 8080
s.connect((host,port))
print("Connected Successfully")

filename = input(str("Please enter a filename for the incoming file: "))
file = open(filename, 'wb')
file_data = s.recv(1024)
file.write(file_data)
file.close()
print("File has been received successfully")