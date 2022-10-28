import getpass
import dbFunctions
import login

aid = None

# Store uid, start the menu


def startMenu(userId):
    global aid
    aid = userId

    menu()
    return


def printMenu():
    print("""
1 - Add a song
2 - Find top fans and playlists
3 - Logout
4 - Exit
Enter a choice and press enter:""")

    return



def menu():
    printMenu()

    while True:
        userInput = int(input())
        if userInput == 1:
            #TODO: Add song
            while True:
                songName = input("Song Name: ")
                songDuration = input("Song Duration: ")
                if not (songDuration.isdigit()):
                    print("Song Duration must be a number try again")
                else:
                    addSong(songName, songDuration)
                    printMenu()
                    break

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

def addSong(songName, songDuration):
    if(dbFunctions.songExists(aid, songName, songDuration)):
        while True:
            addAnyway = input("Song already exists would you like to add it anyways Y/N")
            if (addAnyway.lower() == "n"):
                return
            elif(addAnyway.lower() == "y"):
                break
    
    dbFunctions.addSong(aid, songName, songDuration)
    print("Song added")
    return
