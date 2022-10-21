import getpass
import dbFunctions

# Functionality for starting the login process
def startLogin(): 
    userOrArtistString = input("Type U for User A for Artist: ").lower()
    if (userOrArtistString == "u"):
        registerOrLogin()
    elif (userOrArtistString == "a"):
        login("artists")
    else:
        print("Invalid Input - valid input is U/A \n")
        startLogin()

    return

# Functionality for determing between loging in a user and registering a user
def registerOrLogin():
    resgisterOrLogin = input("are you a returnig user Y/N: ").lower()
    if (resgisterOrLogin == "y"):
        login("users")
    elif (resgisterOrLogin == "n"):
        registerUser()
    else:
        print("Invalid Input - valid input is Y/N \n")
        registerOrLogin()

# Handles the login for existing users and artists (note that type should match the table name)
def login(type):
    id = getId()
    password = input("Passweod: ") #TODO: Replace with getPassword()

    if(dbFunctions.attemptLogin(type, id, password) != "None"):
        # Rediect to correct menu based on type
        print("Logged In")
    else:
        # Retry login
        print("Invalid login - try againn")
        login(type)

    return



# returns the id of the user/artist and type of user (artist or user)
def getLoginInfo():
    userType = ''
    return id, userType

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
    id = getId()
    while checkIfUserExists(id):
        print('That user id is already taken. Please enter a new one')
        id = getId()
    
    name = input('Name: ')
    password = input('Password: ')

def checkIfUserExists(id):
    return False

    