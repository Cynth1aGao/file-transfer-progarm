import socketserver
import threading
import socket
from file_transfer import file_transfer_protocol
# https://www.delftstack.com/howto/python/get-ip-address-python/
# https://www.youtube.com/watch?v=27qfn3Gco00
def str_to_bytes(str):
  return bytes(str, 'utf-8')


def bytes_to_str(data):
  return data.decode('UTF-8')


global_account_dict = {}
global_file_transfer = {}
print("The IP address is: ", socket.gethostbyname(socket.gethostname()))
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class CapitalizeHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = f'{self.client_address} on {threading.currentThread().getName()}'
        print(f'Connected: {client}')
        global_username = ""
        while True:
            recv_list = self.rfile.readline().decode('utf-8').split()
            check = recv_list[0]
            username = recv_list[1]
            password = recv_list[2]
            if check == "create_account":
                if username not in global_account_dict.keys():
                    global_account_dict[username] = [password, False]
                    self.wfile.write(str_to_bytes("succeed"))
                    continue
                else:
                    self.wfile.write(str_to_bytes("create_error"))
            if check == "login":
                if global_account_dict[username][0] != password:
                    self.wfile.write(str_to_bytes("login_error"))
                else:
                    self.wfile.write(str_to_bytes("succeed login"))
                    global_account_dict[username][1] = True
                    global_username = username
                    break
        user1 = file_transfer_protocol(global_username, global_account_dict, global_file_transfer)
        output = ""
        while output != "Bye":
            user_input = bytes_to_str(self.rfile.readline()).strip('\n')
            #print(user_input)
            output = user1.change_state(user_input)
            #print(user1.state)
            #print(output)
            self.wfile.write(str_to_bytes(output))

        filename = ""
        if len(list(global_file_transfer.keys())) > 1:
            for i in global_file_transfer.keys():
                filename = " ".join(i)
        else:
            filename = list(global_file_transfer.keys())[0]

        self.wfile.write(str_to_bytes(filename))
        print(filename)
        if len(list(global_file_transfer.keys())) > 1:
            for i in list(global_file_transfer.keys()):
                file = open(i, 'wb')
                data = self.request.recv(4096)
                file.write(data)
        else:
            file = open(list(global_file_transfer.keys())[0], 'wb')
            data = self.request.recv(4096)
            file.write(data)
'''
    while True:
        user_input = ""
        user1 = file_transfer_protocol(global_account_dict)
        output = user1.change_state(user_input)
        self.wfile.write(str_to_bytes(output))
        user_input = bytes_to_str(self.rfile.readline())
        while user_input != "":
            output = user1.change_state(user_input)
            self.wfile.write(str_to_bytes(output))
            if output == "Bye":
                break
            user_input = bytes_to_str(self.rfile.readline())
    print(f'Closed: {client}')
'''


with ThreadedTCPServer(('', 80), CapitalizeHandler) as server:
    print(f'The capitalization server is running...')
    server.serve_forever()

'''
while True:
    conn, address = x.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (conn, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    user_input = ""
    user1 = file_transfer_protocol(conn, global_account_dict)
    output = user1.change_state(user_input)
    conn.send(str_to_bytes(output))
    while user_input != "":
        user_input = bytes_to_str(conn.recv(4096))
        output = user1.change_state(user_input)
        conn.send(str_to_bytes(output))
        if output == "Bye":
            break

'''



'''
file_name = input(str("Please enter the filename of the file: "))
file = open(file_name, "rb")
data_read = file.read(2048)
conn.send(data_read)
print("File has been sent successfully")
x.close()
'''
