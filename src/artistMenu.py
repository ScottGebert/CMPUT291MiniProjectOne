import getpass
import dbFunctions
import login

uid = None

# Store uid, start the menu


def startMenu(userId):
    global uid
    uid = userId

    menu()
    return


def printMenu():
    print("""
1 - Add a song
2 - Find top fans and playlists
3- Logout
4- Exit
Enter a choice and press enter:""")

    return


def menu():
    printMenu()

    while True:
        userInput = int(input())
        if userInput == 1:
            #TODO: Add song
            print("SessionStart")
        elif userInput == 2:
            #TODO: Find top fans and playlists
            print("Search")
        elif userInput == 3:
            login.getLoginInfo()
        elif userInput == 4:
            break
        else:
            print("Refer to menu")

    return
