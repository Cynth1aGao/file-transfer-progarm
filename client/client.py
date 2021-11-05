import getpass
import socket

# https://stackoverflow.com/questions/35805078/how-do-i-convert-a-password-into-asterisks-while-it-is-being-entered
# https://www.youtube.com/watch?v=27qfn3Gco00

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
        password = input("Enter the password you want to register for this account: ")
        if username not in self.accounts:
          self.accounts[username] = password
          self.login()
          break
        else:
          print("The username you entered already existed, please change to another one")
  def login(self):
    while True:
      user = input("Username: ")
      pwd = input("Password: ")
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
s.connect((host, port))
print("Connected Successfully")

file_name = input(str("Enter the desired filename: "))
file = open(file_name, 'wb')
data = s.recv(2048)
file.write(data)
file.close()
print("File has been received successfully")