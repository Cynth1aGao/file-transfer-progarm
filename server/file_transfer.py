class file_transfer_protocol:
    def __init__(self, global_account_dict):
        self.state = "waiting"
        self.accounts = global_account_dict
        self.current_account = -1
        self.all_check_lists = []
        self.check_list = -1
        self.active_user = []
    def change_state(self, user_input):
        output = ""
        if self.state == "waiting":
            output = "Do you have an account? yes/no: "
            if user_input == "no":
                self.state = "account username"
                output = "Enter the username you want to register for this account: "
            elif user_input == "yes":
                self.state = "login username"
        elif self.state == "account username":
            if user_input in self.accounts:
                output = "The username you entered already existed, please change to another one"
                self.state = "account username"
            else:
                self.accounts[user_input] = None
                self.current_account += 1
                output = "Enter the password you want to register for this account: "
                self.state = "account password"
        elif self.state == "account password":
            self.accounts[self.current_account] = user_input
            output = "You registered the account successfully"
            self.state = "login username"
        elif self.state == "login username":
            output = "Enter your username and password seperated by a space: "
            input_list = user_input.split()
            self.all_check_lists.append(input_list)
            self.check_list += 1
            self.state = "login check"
        elif self.state == "login check":
            if (self.all_check_lists[self.check_list][0] in self.accounts) and (self.all_check_lists[self.check_list][1] == self.accounts.get(self.all_check_lists[self.check_list][0])):
                output = "login successfully"
                self.state = "log in"
            else:
                output = "Enter a correct username or password!"
                self.state = "login username"
        elif self.state == "log in":
            output = "Keep logging in. Type logout if you want to, else click 'Enter'"
            if user_input == "logout":
                self.state = "log out"
            else:
                self.state = "active users"
        elif self.state == "active users":
            output = "Do u want to check the active users? yes/no "
            if user_input == "yes":
                self.state = "user list"
            else:
                self.state = "log in"
        elif self.state == "user list":
            output = self.active_user
            self.state = "choose user"
        elif self.state == "choose user":
            output = "Type the username you choose to transfer the file (Type 'not right now' if you don't )"
            if user_input in self.active_user:
                self.state = "transfer file"
            elif user_input == "not right now":
                self.state = "log in"
            else:
                self.state = "user list"
        elif self.state == "transfer file":
            output = "Bye"

        return output
