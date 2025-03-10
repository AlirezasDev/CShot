import time
import hashlib
import Account_Handling
from Account_Handling import accounts


def retry_on_failure():
    for count in range(3, -1, -1):
        print("\rRetry in ", count, end="")
        time.sleep(1)

class Signup(Account_Handling.Player):
    def __init__(self):
        super().__init__()
        self.run()

    def run(self):
        while True:
            self.email = input("Enter your email: ").strip()
            if any(members["email"] == self.email for members in accounts.accounts_list):
                print("This email already exists!")
                retry_on_failure()
            elif self.check_mail():
                break
            else:
                print("Invalid email format.")
                retry_on_failure()

        while True:
            self.username = input("Enter your username: ").strip()
            if any(members["username"] == self.username for members in accounts.accounts_list):
                print("This username already exists! Try another one.")
                retry_on_failure()
            elif self.check_username():
                break
            else:
                print("Username must be at least 4 characters long (and less than 20), which can include letters, numbers and underline.")
                retry_on_failure()

        while True:
            self.hashed_password = input("Enter your password: ").strip()
            if self.check_password():
                self.hash_password(self.hashed_password)
                break
            else:
                print("Invalid password. Password must contain at least 8 characters,"
                      " including an uppercase letter, a lowercase letter, a digit, and a special character.")
                retry_on_failure()

        accounts.accounts_list.append({
            "username": self.username,
            "email": self.email,
            "password": self.hashed_password,
            "points": 0,
            "wins": 0,
            "losses": 0,
        })
        accounts.save_accounts()
        print("Signup successful!")

class Login(Account_Handling.Player):
    def __init__(self):
        super().__init__()
        self.run()

    def run(self):

        while True:
            email_or_username = input("Enter your email or username: ").strip()
            found = False  # Flag to check if user is found
            for members in accounts.accounts_list:
                if members["username"] == email_or_username:
                    self.username = email_or_username
                    self.email = members["email"]
                    self.hashed_password = members["password"]
                    found = True
                    break
                elif members["email"] == email_or_username:
                    self.username = members["username"]
                    self.email = email_or_username
                    self.hashed_password = members["password"]
                    found = True
                    break

            if not found:
                print("Email or username not found! Please try again.")
                retry_on_failure()
                continue

            break

        while True:
            password = input("Enter your password: ")
            if hashlib.sha256(password.encode()).hexdigest() == self.hashed_password:
                print(f"Welcome back, {self.username}!")
                break
            else:
                print("Incorrect password.")
                retry_on_failure()

        print("Login successful!")

