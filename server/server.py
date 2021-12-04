import socketserver
import threading
import socket
import os
import os.path

from file_transfer import file_transfer_protocol
# https://www.delftstack.com/howto/python/get-ip-address-python/
# https://www.youtube.com/watch?v=27qfn3Gco00
def str_to_bytes(str):
  return bytes(str, 'utf-8')


def bytes_to_str(data):
  return data.decode('UTF-8')

# The key is the username, the first element in the corresponding key's values is pasword, the second element is active status: True for active, False for not
global_account_dict = {}
# The key the name of the file need to be transferred,the first element in the corresponding key's values is sender username, second element is receiver's username
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
            # keep receiving username and password when register account and log in
            recv_list = self.rfile.readline().decode('utf-8').split()
            check = recv_list[0]
            username = recv_list[1]
            password = recv_list[2]

            # if the username and password stored in the recv_list used for registering a new account
            # Add the username as a key in the global_account_dict, set the first element in the value list equals to password
            # Set the username active status to default - False
            if check == "create_account":
                if username not in global_account_dict.keys():
                    global_account_dict[username] = [password, False]
                    # send to the client that registering succeed
                    self.wfile.write(str_to_bytes("succeed"))
                    continue
                else:
                    # if username already exists in the global_account_dict, send to the client the error
                    self.wfile.write(str_to_bytes("create_error"))
            if check == "login":
                if global_account_dict[username][0] != password:
                    # send to the client the error that the username not matched the password stored in the account_dict
                    self.wfile.write(str_to_bytes("login_error"))
                else:
                    self.wfile.write(str_to_bytes("succeed login"))
                    # Set the user's active status to True
                    global_account_dict[username][1] = True
                    global_username = username
                    break

        # receive the client's username if the client wants to check the box
        show_file = bytes_to_str(self.rfile.readline()).strip('\n')
        print("show_file", show_file)
        # find the current dictionary
        cur_dir = os.getcwd()
        file_list = os.listdir(cur_dir)
        check_file = "Your box is empty and "
        accum_file = 0
        transfer_file = []
        # if client wants to check the box
        if show_file != "no":
            for file in file_list:
                if "#" in file:
                    print("file in file list: ", file)
                    # check whether there is a file in the server that needs to be transferred to that user
                    file_split = file.split("#")
                    if file_split[1] == show_file:
                        print("filter out", file_split[1])
                        check_file = "Your box is not empty and "
                        accum_file += 1
                        # append that file to the transfer_file list
                        transfer_file.append(file)

            # send client the information of the client's box
            self.wfile.write(str_to_bytes(check_file + "there are " + str(accum_file) + " file/files."))
            print(str_to_bytes(check_file + "there are " + str(accum_file) + " file/files."))
            # information received from the client to check whether the client wants to download the file in the box
            download = bytes_to_str(self.rfile.readline()).strip('\n')
            if download == "yes":
                # download all the files in the box
                for file in transfer_file:
                    file_download = open(file, "rb")
                    data_read = file_download.read(4096)
                    self.wfile.write(data_read)




        user1 = file_transfer_protocol(global_username, global_account_dict, global_file_transfer)
        output = ""
        while output != "Bye":
            user_input = bytes_to_str(self.rfile.readline()).strip('\n')
            output = user1.change_state(user_input)
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
                file_name = str(global_file_transfer.get(i)[0]) + "#" + str(global_file_transfer.get(i)[1]) + "#" + str(i)
                file = open(file_name, 'wb')
                data = self.request.recv(4096)
                file.write(data)
                file.close()
        else:
            filename = str(global_file_transfer.get(list(global_file_transfer.keys())[0])[0]) + "#" + str(global_file_transfer.get(list(global_file_transfer.keys())[0])[1]) + "#" + str(list(global_file_transfer.keys())[0])
            file = open(filename, 'wb')
            data = self.request.recv(4096)
            file.write(data)
            file.close()
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
