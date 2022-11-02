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
6 - Exit
Enter a choice and press enter:""")

    return


def menu():    
    while True:
        printMenu()
        userInput = int(input())

        # start session
        if userInput == 1:
            print("SessionStart")            
            dbFunctions.startSession(uid)

        # Search for song/playlist
        elif userInput == 2:
            line = input("Enter keywords for a song or playlist: ")
            keywords = line.split()
            matchingValues = dbFunctions.searchSongsAndPlaylists(keywords)
            if matchingValues == None or len(matchingValues) < 1:
                print("No songs or playlists matched the keywords given")
                continue            
            
            print("There were " + str(len(matchingValues)) + " search results")
            matchesDict = dict((i, match) for i, match in enumerate(matchingValues, 1))  

            # only print the first 5 matches         
            for i, match in matchesDict.items():
                if i > 5:
                    print("6 - See the rest of the list")
                    break
                print(str(i) + " - " + ' | '.join(map(str, match)))
            
            selection = int(input("Select an option: "))
            
            # this means that 6 was see the rest of the list
            if selection == 6 and len(matchingValues) > 5:
                for i, match in matchesDict.items():                
                    print(str(i) + " - " + ' | '.join(map(str, match)))
                
                selection = int(input("Select an option: "))

            if selection <= len(matchingValues):
                if matchesDict[selection][3] == 'Song':
                    songActions(matchesDict[selection])
                else:
                    songs = dbFunctions.getSongsInPlaylist(matchesDict[selection][0])
                    if songs == None:
                        print(matchesDict[selection][1] + " does not have any songs")
                        continue

                    print(matchesDict[selection][1] + " has " + str(len(songs)) + " songs")
                    songsDict = dict((i, match) for i, match in enumerate(songs, 1))           
                    for i, match in songsDict.items():
                        print(str(i) + " - " + ' | '.join(map(str, match)))
                    
                    selection = int(input("Select an option: "))

                    if selection <= len(songs):
                        songActions(songsDict[selection])

        # search for artists
        elif userInput == 3:
            line = input("Enter keywords for an artist: ")
            keywords = line.split()
            artists = dbFunctions.searchArtists(keywords)
            if artists == None or len(artists) < 1:
                print("No artists or songs matched the keywords given")
                continue

            print("There were " + str(len(artists)) + " search results")
            artistsDict = dict((i, match) for i, match in enumerate(artists, 1))           
            for i, match in artistsDict.items():
                if i > 5:
                    print("6 - See the rest of the list")
                    break
                print(str(i) + " - " + ' | '.join(map(str, match[1:]))) # don't print the aid
            
            selection = int(input("\nSelect an option: "))
            
            # this means that 6 was see the rest of the list
            if selection == 6 and len(artists) > 5:
                for i, match in artistsDict.items():                
                    print(str(i) + " - " + ' '.join(map(str, match[1:]))) # don't print the aid
                
                selection = int(input("Select an option: "))
            
            if selection <= len(artists):
                songs = dbFunctions.getArtistsSongs(artistsDict[selection][0])
                if songs == None or len(songs) < 1:
                    print(artistsDict[selection][1] + " does not have any songs")
                    continue

                print(artistsDict[selection][1] + " has " + str(len(songs)) + " songs")
                songsDict = dict((i, match) for i, match in enumerate(songs, 1))           
                for i, match in songsDict.items():
                    print(str(i) + " - " + ' | '.join(map(str, match)))
                
                selection = int(input("\nSelect an option: "))

                if selection <= len(songs):
                    songActions(songsDict[selection])
            
        elif userInput == 4:
            dbFunctions.endSession(uid)
        elif userInput == 5:
            if dbFunctions.getActiveSession(uid) != None:
                dbFunctions.endSession(uid)
            return 0 # 0 means log out
        elif userInput == 6:
            if dbFunctions.getActiveSession(uid) != None:
                dbFunctions.endSession(uid)
            return 1 # 1 means exit
        else:
            print("Invalid input. Refer to menu")

    
# function that performs all necessary actions for a song.
# song input is a list with entries [sid, title, duration]
def songActions(song):
    print(song[1] + " was selected")

    while True:
        printSongActionMenu()
        selection = int(input("Select an option: "))

        while selection < 1 or selection > 4:
            print("Invalid selection")
            selection = int(input("Select an option: "))

        # listen to song
        if selection == 1:
            dbFunctions.listenToSong(uid, song)
        
        # see more info about song
        elif selection == 2:
            print("id = " + str(song[0]))
            print("title = " + song[1])
            print("duration = " + str(song[2]))

            artists = dbFunctions.getArtistsFromSong(song[0])
            print("artists performed by: " + ', '.join(artists))
            

            playlists = dbFunctions.getPlaylistsFromSong(song[0])
            if playlists == None or len(playlists) < 1:
                print(song[1] + " is not present in any playlists")
            else:
                print("playlists that " + song[1] + " is in: " + ', '.join(playlists))

        # add song to playlist
        elif selection == 3:
            printAddToPlaylistMenu()

            plSelection = int(input("Select an option: "))
            while plSelection < 1 or plSelection > 3:
                print("Invalid selection")
                plSelection = int(input("Select an option: "))
            
            if plSelection == 1:
                playlists = dbFunctions.getPlaylistsFromUid(uid)
                if len(playlists) < 1:
                    print("You do not have any playlists")
                    while True:
                        yn = input("Would you like to create a new playlist ? Y/N: ")
                        if (yn.lower() == "y"):
                            plSelection = 2
                            break
                        elif (yn.lower() == "n"):
                            plSelection = 3 # just go back
                            break
                else:
                    print("Here is a list of the playlists you own")
                    print("   |ID| Title ")
                    playlistsDict = dict((i, match) for i, match in enumerate(playlists, 1))
                    for i, pl in playlistsDict.items():
                        print(str(i) + " - " + str(pl[0]) + "| " + pl[1])
                    
                    option = int(input("Select an option: "))                    
                    while option not in playlistsDict:
                        print("Invalid selection")
                        option = int(input("Select an option: "))
                    
                    dbFunctions.addSongToPlaylist(song[0], playlistsDict[option][0])

            # not elif incase user selects 1 and no playlists exist
            if plSelection == 2:
                title = input("\nEnter a title for your new playlist: ")
                pid = dbFunctions.createNewPlaylist(uid, title)
                dbFunctions.addSongToPlaylist(song[0], pid)
            elif plSelection == 3:
                continue

        else:
            return


# prints a list of all song actions
def printSongActionMenu():
    print("""
1 - Listen to song
2 - See more information about song
3 - Add song to playlist
4 - Back
    """)


# prints a list of options for a playlist
def printAddToPlaylistMenu():
    print("""
1 - Add to existing playlist
2 - Add to new playlist
3 - Back
    """)

