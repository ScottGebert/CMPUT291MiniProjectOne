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
1 - Start a session
2 - Search for songs and playlists
3 - Search for artists
4 - Logout
5 - Exit
Enter a choice and press enter:""")

    return

def menu():
    printMenu()

    userInput = int(input())
    if userInput == 1:
        #TODO: Start a session
        print("SessionStart")
    elif userInput == 2:
        #TODO: Playlist and song search
        print("Search")
    elif userInput == 3:
        #TODO: artist search
        print("SearchArtist")
    elif userInput == 4:
        login.startLogin()
    elif userInput == 5:
        exit()
    else:
        print("Refer to menu")

    return

def exit():
     #TODO: End active sessions
    print("exiting")
    return