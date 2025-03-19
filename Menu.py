import time
import keyboard
from printy import printy
import os
import hashlib
from Account_Handling import Player
from Account_Handling import accounts


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def retry_on_failure():
    for count in range(3, -1, -1):
        print("\rRetry in ", count, end="")
        time.sleep(1)

class Signup(Player):
    def __init__(self):
        super().__init__()
        self.run()

    def run(self):
        while True:
            clear_terminal()
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
            clear_terminal()
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
            clear_terminal()
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

class Login(Player):
    def __init__(self):
        super().__init__()
        self.run()

    def run(self):

        while True:
            clear_terminal()
            email_or_username = input("Enter your email or username: ").strip()

            if type(p1) != str:
                if email_or_username in [p1.username, p1.email]:
                    print("User already logged in.")
                    retry_on_failure()
                    continue

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
            clear_terminal()
            password = input("Enter your password: ")
            if hashlib.sha256(password.encode()).hexdigest() == self.hashed_password:
                print(f"Welcome back, {self.username}!")
                break
            else:
                print("Incorrect password.")
                retry_on_failure()

        print("Login successful!")


class Menu:
    def __init__(self, options):
        self.options = options
        self.current_selection = 0

    def display_menu(self):
        clear_terminal()
        printy("-use the 'arrow keys' to navigate.", "g")
        printy("-use the 'space bar' to confirm your selection.", "g")
        print("\n")

        for index, option in enumerate(self.options):
            if index == self.current_selection:
                printy("\t->" + f"[mBHI]{option}@")
            else:
                printy("\t" + option, "B")
            print("\n")
        print("\n")

    def navigate_menu(self):
        self.display_menu()
        while True:
            if keyboard.is_pressed('up'):
                self.current_selection = (self.current_selection - 1) % len(self.options)
                self.display_menu()
                time.sleep(0.2)
            elif keyboard.is_pressed('down'):
                self.current_selection = (self.current_selection + 1) % len(self.options)
                self.display_menu()
                time.sleep(0.2)
            elif keyboard.is_pressed('space'):
                time.sleep(0.2)
                return self.selection()

    def selection(self):
        global p2, p1
        selection = self.options[self.current_selection]
        if selection == "Login (P1)":
            p1 = Login()
            P2_menu.navigate_menu()
            return
        elif selection == "Signup (P1)":
            p1 = Signup()
            P2_menu.navigate_menu()
            return
        elif selection == "Login (P2)":
            p2 = Login()
            return
        elif selection == "Signup (P2)":
            p2 = Signup()
            return
        elif selection == "Quit":
            return self.confirm_quit()
        elif selection == "Leaderboard":
            Menu.leaderboard()
            return
        elif selection == "Main Menu":
            main_menu.navigate_menu()
            return

    def confirm_quit(self):
        while True:
            clear_terminal()
            yorn = input("Are you sure you want to quit?(y/n)").strip().lower()
            if yorn == "y":
                for count in range(3):
                    for i in range(4):
                        print("\rExiting the app" + "." * i + " " * (3 - i), end="")
                        time.sleep(0.45)
                clear_terminal()
                print("\rBye!", end="")
                time.sleep(1)
                exit()
            elif yorn == "n":
                return self.navigate_menu()

    def leaderboard():
        clear_terminal()
        users = accounts.accounts_list
        sorted_users = sorted(users, key=lambda x: x["points"], reverse=True)

        printy("=" * 36 + "TOP 3 PLAYERS" + "=" * 36, "BHw")
        printy(" {:30}{:<20}{:<15}{:<19}".format("Username", "Points", "Wins", "Losses"), "BH")

        try:
            printy("  {:30}{:<+20}{:<16}{:<17}".format(sorted_users[0]['username'], sorted_users[0]['points'],
                                                             sorted_users[0]['wins'], sorted_users[0]['losses']), "BHy")
        except:
            pass
        try:
            printy("  {:30}{:<+20}{:<16}{:<17}".format(sorted_users[1]['username'], sorted_users[1]['points'],
                                                             sorted_users[1]['wins'], sorted_users[1]['losses']), "BHc")
        except:
            pass
        try:
            printy("  {:30}{:<+20}{:<16}{:<17}".format(sorted_users[2]['username'], sorted_users[2]['points'],
                                                             sorted_users[2]['wins'], sorted_users[2]['losses']), "BHm")
        except:
            pass

        printy("press 'q' to quit", "D")
        printy("press 'm' to go back to the main menu", "D")

        while True:
            if keyboard.is_pressed('q'):
                for count in range(3):
                    for i in range(4):
                        print("\rExiting the app" + "." * i + " " * (3 - i), end="")
                        time.sleep(0.45)
                clear_terminal()
                print("\rBye!", end="")
                time.sleep(1)
                exit()

            if keyboard.is_pressed('m'):
                main_menu.navigate_menu()


p1 = ""
p2 = ""

P2_menu = Menu(["Login (P2)", "Signup (P2)", "Quit"])
main_menu = Menu(["Login (P1)", "Signup (P1)", "Leaderboard", "Quit"])
main_menu.navigate_menu()



