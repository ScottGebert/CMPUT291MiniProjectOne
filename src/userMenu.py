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
            dbFunctions.startSession(uid)

        elif userInput == 2:
            line = input("Enter keywords for a song or playlist: ")
            keywords = line.split()
            matchingValues = dbFunctions.searchSongsAndPlaylists(keywords)
            if matchingValues == None:
                print("No songs or playlists matched the keywords given")
                continue

            print("There were " + str(len(matchingValues)) + " search results")
            matchesDict = dict((i, match) for i, match in enumerate(matchingValues, 1))           
            for i, match in matchesDict.items():
                if i > 5:
                    print("6 - See the rest of the list")
                    break
                print(str(i) + " - " + ' '.join(map(str, match)))
            
            selection = int(input("Select an option: "))
            
            # this means that 6 was see the rest of the list
            if selection == 6 and len(matchingValues) > 5:
                for i, match in matchesDict.items():                
                    print(str(i) + " - " + ' '.join(map(str, match)))
                
                selection = int(input("Select an option: "))

            if selection <= len(matchingValues):
                if matchesDict[selection][3] == 'Song':
                    songActions(matchesDict[selection])
                else:
                    print(' '.join(map(str, matchesDict[selection])))

        elif userInput == 3:
            #TODO: artist search
            print("SearchArtist")
        elif userInput == 4:
            dbFunctions.endSession(uid)
        elif userInput == 5:
            if dbFunctions.getActiveSession(uid) != None:
                dbFunctions.endSession(uid)
            return
        else:
            print("Invalid input. Refer to menu")

    

def songActions(song):
    print(song[1] + " was selected")

    while True:
        printSongActionMenu()
        selection = int(input("Select an option: "))

        while selection < 1 or selection > 4:
            print("Invalid selection")
            selection = int(input("Select an option: "))

        if selection == 1:
            dbFunctions.listenToSong(uid, song)
        elif selection == 2:
            print("id = " + str(song[0]))
            print("title = " + song[1])
            print("duration = " + str(song[2]))

            artists = dbFunctions.getArtistsFromSong(song[0])
            print("artists performed by: " + ', '.join(artists))
            

            playlists = dbFunctions.getPlaylistsFromSong(song[0])
            if playlists != None:
                print("playlists that song is in: " + ', '.join(playlists))

        elif selection == 3:
            print("Add to playlist")
        else:
            return


def printSongActionMenu():
    print("""
1 - Listen to song
2 - See more information about song
3 - Add song to playlist
4 - Back
    """)

