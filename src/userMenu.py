import getpass
import dbFunctions
import MiniProjectOne

uid = None

# Store uid start the menu


def startMenu(userId):
    global uid
    uid = userId

    menu()
    return


def printMenu():
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
    while True:
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
            MiniProjectOne.main()
        elif userInput == 5:
            exit()
            break
        else:
            print("Refer to menu")

    return


def exit():
    #TODO: End active sessions
    print("exiting")
    return
