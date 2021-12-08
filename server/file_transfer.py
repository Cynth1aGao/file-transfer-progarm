class file_transfer_protocol:
    def __init__(self, username, global_account_dict, global_file_transfer):
        self.username = username
        self.state = "log in"
        self.accounts = global_account_dict
        self.active_user = {}
        self.active_user = set()
        self.user_choose = ""
        self.file_transfer = global_file_transfer
    def change_state(self, user_input):
        output = ""
        if self.state == "log in":
            self.accounts[self.username][1] = True
            if user_input == "log out":
                output = "Bye"
                self.accounts[self.username][1] = False
            elif user_input == "check_active_users":
                for i in self.accounts.items():
                    if i[1][1] == True:
                        self.active_user.add(i[0])
                output = "Here is the list of active user: [" + ' '.join(
                    self.active_user) + "]. Type the username you want to choose to transfer the file or type 'not right now' if you don't want to transfer the file rigt now:"
                self.state = "choose user"
            elif user_input == "check_box":
                output = "show_box"
                self.state = "log in"
            else:
                output = "Incorrect input! Please type again: "
                self.state = "log in"
        elif self.state == "choose user":
            if user_input in self.active_user:
                self.user_choose = user_input
                output = "Great! Type in the filename of the file you want to transfer:"
                self.state = "transfer file"
            elif user_input == "not right now":
                output = "Ok! You can keep log in. Type log out if you want to log out, type check_active_users to check active users and type check_box to see your file box"
                self.state = "log in"
            else:
                output = "Type wrong username! Please try again: "
                self.state = "choose user"
        elif self.state == "transfer file":
            # first value in the value list is sender's username, second value is the receiver's username
            self.file_transfer[user_input] = [self.username, self.user_choose]
            output = "File already transferred!Type 'log out' if you want to log out, type 'user list' to check other active users:"
            self.state = "log out"
        elif self.state == "log out":
            if user_input == "user list":
                output = "Here is the list of active user: [" + ' '.join(self.active_user) + "]. Type the username you want to choose to transfer the file or type 'not right now' if you don't want to transfer the file rigt now:"
                self.state = "choose user"
            else:
                self.accounts[self.username][1] = False
                output = "Bye"

        return output