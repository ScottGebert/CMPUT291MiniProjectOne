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
4 - End a session
5 - Logout
Enter a choice and press enter:""")

    return


def menu():    
    while True:
        printMenu()
        userInput = int(input())

        if userInput == 1:
            print("SessionStart")
            nextSessionNo = dbFunctions.getNextUnusedId('sessions', 'sno')
            if nextSessionNo == None:
                nextSessionNo = 1
            
            dbFunctions.startSession(uid, nextSessionNo)
        elif userInput == 2:
            line = input("Enter keywords for a song or playlist: ")
            keywords = line.split()
            
        elif userInput == 3:
            #TODO: artist search
            print("SearchArtist")
        elif userInput == 4:
            dbFunctions.endSession(uid)
        elif userInput == 5:
            return
        else:
            print("Invalid input. Refer to menu")

    return

