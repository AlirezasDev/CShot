import json
import re
import hashlib

class AccountHandling:
    def __init__(self, filepath):
        self.filepath = filepath
        self.accounts_list = []

    def load_accounts(self):
        with open(self.filepath, "r") as data:
            self.accounts_list = json.load(data)
            return

    def save_accounts(self):
        with open(self.filepath, "w") as data:
            json.dump(self.accounts_list, data, indent=4)
            return


class Player:
    def __init__(self):
        self.username = ""
        self.email = ""
        self.hashed_password = ""

    def check_mail(self):
        pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
        return bool(re.match(pattern, self.email))

    def check_password(self):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!_]).{8,}$"
        return bool(re.match(pattern, self.hashed_password))

    def check_username(self):
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$'
        return bool(re.match(pattern, self.username))

    def hash_password(self, password):
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()

    def assign_point(self, score, win_status):
        for member in accounts.accounts_list:
            if member["username"] == self.username:
                if win_status == "W":
                    member["wins"] += 1
                elif win_status == "L":
                    member["losses"] += 1
                member["points"] += score
                accounts.save_accounts()



accounts = AccountHandling("account.json")
accounts.load_accounts()
