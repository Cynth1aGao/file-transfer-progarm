global_account_dict = {}

class file_transfer_protocol:
    def __init__(self):
        self.state = "waiting"
        self.accounts = global_account_dict
        self.current_account = -1
        self.all_check_lists = []
        self.check_list = -1

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
            else:
                output = "Enter a correct username or password!"
                self.state = "login username"
        return output
