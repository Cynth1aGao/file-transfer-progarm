import socketserver
import threading
import socket

# https://www.delftstack.com/howto/python/get-ip-address-python/
# https://www.youtube.com/watch?v=27qfn3Gco00
def str_to_bytes(str):
  return bytes(str, 'utf-8')


def bytes_to_str(data):
  return data.decode('UTF-8')

print("The IP address is: ", socket.gethostbyname(socket.gethostname()))
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class CapitalizeHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = f'{self.client_address} on {threading.currentThread().getName()}'
        print(f'Connected: {client}')
        while True:
            data = self.rfile.readline()
            if not data:
                break
            self.wfile.write(data.decode('utf-8').upper().encode('utf-8'))
        print(f'Closed: {client}')

with ThreadedTCPServer(('', 5090), CapitalizeHandler) as server:
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
