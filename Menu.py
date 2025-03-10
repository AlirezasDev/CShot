import time
import keyboard
from printy import printy
import os
import Signup_Login


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        global player2, player1
        selection = self.options[self.current_selection]
        if selection == "Login (P1)":
            player1 = Signup_Login.Login()
            P2_menu.navigate_menu()
            return
        elif selection == "Signup (P1)":
            player1 = Signup_Login.Signup()
            P2_menu.navigate_menu()
            return
        elif selection == "Login (P2)":
            player2 = Signup_Login.Signup()
            return
        elif selection == "Signup (P2)":
            player2 = Signup_Login.Signup()
            return
        elif selection == "Quit":
            return self.confirm_quit()
        elif selection == "Leaderboard":
            return
        elif selection == "Main Menu":
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


player1 = ""
player2 = ""

main_menu = Menu(["Login (P1)", "Signup (P1)", "Leaderboard", "Quit"])
main_menu.navigate_menu()

P2_menu = Menu(["Login (P2)", "Signup (P2)", "Quit"])

