import getpass
import dbFunctions

# Functionality for starting the login process
# returns the id of the user/artist and type of user (artist or user)


def getLoginInfo():
    while True:
        id = getId()
        password = input("Password: ")  # getPassword() returns err currently

        if (dbFunctions.idInBoth(id)):
            userOrArtist = ""
            while True:
                userOrArtist = input(
                    "ID was found in both tables are you logging in as a User or Artist U/A: ")
                if (userOrArtist == "u"):
                    if (dbFunctions.loginUser(id, password)):
                        return "user", id
                    else:
                        print("Login Failed")
                        break
                elif (userOrArtist == "a"):
                    if (dbFunctions.loginArtist(id, password)):
                        return "artist", id
                    else:
                        print("Login Failed")
                        break
        else:
            result = dbFunctions.attemptLoginBothTables(id, password)
            print(result, id)
            if (result != None):
                return result, id
                break

            if (result == None):
                register = None
                while True:
                    register = input(
                        "Would you like to register as a new user? Y/N: ")
                    if (register.lower() == "y"):
                        uid = registerUser()
                        return "user", uid
                    elif (register.lower() == "n"):
                        break


def displayWelcome():
    title = '''
    ************************************
    *                                  *
    *            Welcome!              *
    *                                  *
    ************************************
    '''

    print(title)


def getId():
    id = input('ID: ')
    return id


def getPassword():
    try:
        password = getpass()
    except Exception as error:
        print('Error: ', error)
    else:
        print(password)
        return password


def registerUser():
    print("New User Registration")
    id = getId()
    while dbFunctions.checkUserId(id):
        print('That user id is already taken. Please enter a new one')
        id = getId()

    name = input('Name: ')
    password = input('Password: ')

    dbFunctions.registerUser(id, name, password)

    return id
