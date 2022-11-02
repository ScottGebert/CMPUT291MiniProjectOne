import getpass
import dbFunctions
import login
import MiniProjectOne
import userMenu

aid = None

def printMenu():
    print("""
1 - Add a song
2 - Find top fans and playlists
3 - Logout
4 - Exit
Enter a choice and press enter:""")

    return


def menu(userId):
    global aid
    aid = userId
    
    printMenu()
    while True:
        userInput = int(MiniProjectOne.getInput("", "Must make a selection"))
        if userInput == 1:
            while True:
                songName = MiniProjectOne.getInput("Song Name: ", "Song name cannot be blank")
                songDuration = MiniProjectOne.getInput("Song Duration: ", "Song Duration cannot be blank")
                if not (songDuration.isdigit()):
                    print("Song Duration must be a number try again")
                else:
                    addSong(songName, songDuration)
                    printMenu()
                    break

        elif userInput == 2:
            # For now top playlists and top users is one command - can be split into 2 just add a number and
            # seperate function calls
            getTopPlaylists()
            getTopUsers()
            printMenu()
        elif userInput == 3:
            return True
        elif userInput == 4:
            return False
        else:
            print("Refer to menu")

    return


def addSong(songName, songDuration):
    if (dbFunctions.songExists(aid, songName, songDuration)):
        while True:
            addAnyway = MiniProjectOne.getInput(
                "Song already exists would you like to add it anyways Y/N", "Must select Y/N")
            if (addAnyway.lower() == "n"):
                return
            elif (addAnyway.lower() == "y"):
                break

    dbFunctions.addSong(aid, songName, songDuration)
    print("Song added!")
    return


def getTopPlaylists():
    rows = dbFunctions.getTopPlaylists(aid)
    if (rows != None):
        print("Top Playlists:")
        i = 1
        for row in rows:
            print("   ", i, row[0])
            i = i + 1
    else:
        print("None of your songs appear in any playlists")


def getTopUsers():
    rows = dbFunctions.getTopUsers(aid)
    if (rows != None):
        print("Top Fans:")
        i = 1
        for row in rows:
            print("   ",i, row[0])
            i = i + 1
    else:
        print("No users have listend to your music yet")
