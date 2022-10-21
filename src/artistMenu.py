import getpass
import dbFunctions
import login

uid = None
name = None

# Store uid and name, start the menu
def startMenu(userId, userName):
    global uid, name
    uid = userId
    name = userName

    menu()
    return 

def  printMenu():
    print("""
1 - Add a song
2 - Find top fans and playlists
3- Logout
4- Exit
Enter a choice and press enter:""")

    return

def menu():
    printMenu()

    userInput = int(input())
    if userInput == 1:
        #TODO: Add song 
        print("SessionStart")
    elif userInput == 2:
        #TODO: Find top fans and playlists
        print("Search")
    elif userInput == 3:
        login.startLogin()
    elif userInput == 4:
        print("Exiting")
    else:
        print("Refer to menu")

    return