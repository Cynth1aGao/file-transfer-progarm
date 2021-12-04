import sys
import socket
# https://stackoverflow.com/questions/35805078/how-do-i-convert-a-password-into-asterisks-while-it-is-being-entered
# https://www.youtube.com/watch?v=27qfn3Gco00

def str_to_bytes(data):
  return data.encode('utf-8')


def bytes_to_str(data):
  return data.decode('UTF-8')

# Helper function for user to register an account
def register_account():
    username = input("Enter the username you want to register for this account: ")
    password = input("Enter the password you want to register for this account: ")
    combine = "create_account " + " ".join([username, password]) + "\n"
    sock.sendall(str_to_bytes(combine))

def check_box():
    check_file = str(input("Do you want to check whether you have file in the box? yes/no: "))
    if check_file == "yes":
        # send to the server the client's username
        client_send = username + "\n"
        sock.sendall(str_to_bytes(client_send))
        box_info = bytes_to_str(sock.recv(4096))
        print(box_info)
        split_list = box_info.split()
        if split_list[7] != "0":
            download = str(input("Do you want to download the files? yes/no: "))
            sock.sendall(str_to_bytes(download + "\n"))
            if download == "yes":
                for i in range(int(split_list[8])):
                    file = open("receive_file.txt", 'wb')
                    data = sock.recv(4096)
                    file.write(data)
                    file.close()
    else:
        sock.sendall(str_to_bytes("no" + "\n"))

def transfer_file():
    filename = bytes_to_str(sock.recv(4096))
    file = open(filename, "rb")
    data_read = file.read(4096)
    sock.sendall(data_read + str_to_bytes("\n"))


# Helper function for user to log in
def login():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    combine = "login " + " ".join([username, password]) + "\n"
    sock.sendall(str_to_bytes(combine))
    return username

ip_addr = str(input("Please enter the server ip address you want to connect: "))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((ip_addr, 80))
    print('Enter lines of text then Ctrl+D or Ctrl+C to quit')


    account_check = str(input("Do you have an account? yes/no: "))

    # if user doesn't have an account, register the account first
    if account_check == "no":
        while True:
            register_account()
            data = bytes_to_str(sock.recv(4096))
            # if username already exists, ask the user to create account again
            if data == "create_error":
                print("The username already existed, please choose another one")
            # else account registering succeed go to the log in part
            elif data == "succeed":
                break

    print("Log in: ")
    # if user has an account, log in
    while True:
        username = login()
        data = bytes_to_str(sock.recv(4096))
        if data == "login_error":
            print("Wrong username or password, try again")
        elif data == "succeed login":
            break
    print("You log in to your account successfully")

    userinput = str(input("Here is the main menu: check_box; check_active_users; log out. Type what do you want: "))
    while True:
        if userinput == "check_box":
            sock.sendall(str_to_bytes(userinput + "\n"))
            check_box()
            userinput = str(input("Here is the main menu: check_box; check_active_users; log out. Type what do you want: "))
        sock.sendall(str_to_bytes(userinput + "\n"))
        print_data = bytes_to_str(sock.recv(4096))
        if print_data == "File already transferred!Type 'log out' if you want to log out, type 'user list' to check other active users:":
            transfer_file()
        print(print_data)
        if print_data == "Bye":
            break
        userinput = str(input())

