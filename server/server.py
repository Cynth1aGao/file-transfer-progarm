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

class filetransfer:
  def __init__(self):
    self.accounts = {}
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
        if username_str not in self.accounts:
          self.accounts[username_str] = password_str
          self.login()
          break
        else:
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

user1 = filetransfer()
user1.create_account()
file_name = input(str("Please enter the filename of the file: "))
file = open(file_name, "rb")
data = file.read(2048)
conn.send(data)
print("File has been sent successfully")