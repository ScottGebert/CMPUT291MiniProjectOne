import sqlite3
import time

connection = None
cursor = None


def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return cursor


### LOGIN FUNCTIONS ###
# Returns the userType if login is sucsessful otherwise returns None
def attemptLoginBothTables(id, pwd):
    userType = None
    if (loginUser(id, pwd)):
        userType = "user"
    elif (loginArtist(id, pwd)):
        userType = "artist"

    return userType


# Check is id is in both users and artists
def idInBoth(id):
    cursor.execute(f"""SELECT uid as id FROM users WHERE uid='{id}'
                        UNION ALL
                        SELECT aid as id FROM artists WHERE aid='{id}';""")

    rows = cursor.fetchall()
    return True if len(rows) > 1 else False


# Returns True if login is sucsessful
def loginUser(id, pwd):
    cursor.execute(f"""SELECT * FROM users WHERE uid='{id}' and pwd='{pwd}'""")
    row = cursor.fetchone()
    return (False if row == None else True)


# Returns True if login is sucsessful
def loginArtist(id, pwd):
    cursor.execute(
        f"""SELECT * FROM artists WHERE aid='{id}' and pwd='{pwd}'""")
    row = cursor.fetchone()
    return (False if row == None else True)


# User ID can match aid so only check Users
def checkUserId(id):
    cursor.execute(f"""SELECT * FROM users WHERE uid='{id}'""")
    row = cursor.fetchone()
    return (False if row == None else True)


def registerUser(id, name, password):
    cursor.execute(
        f"""INSERT into users VALUES ("{id}", "{name}", "{password}");""")
   
    connection.commit()
    
    return


### ARTIST FUNCTIONS ###
def songExists(aid, songName, songDuration):
    cursor.execute(
        f"""SELECT count(*) as count FROM songs INNER JOIN perform on songs.sid = perform.sid
        where perform.aid='{aid}' and Lower(songs.title)='{songName}' AND songs.duration={songDuration};""")

    count = cursor.fetchone()
    
    print(count)

    return (True if count[0] > 0 else False)


def addSong(aid, songName, songDuration):
    sid = getNextUnusedId('songs', 'sid')
    
    cursor.execute(
        f"""INSERT into songs VALUES ({sid}, "{songName}", {songDuration} );""")

    cursor.execute(
        f"""INSERT into perform VALUES ("{aid}",{sid});""")
    
    connection.commit()
    
    return

### ALL FUNCTIONS ###
# Only works if the PK is an int
def getNextUnusedId(tableName, idColumnName):
    cursor.execute(
        f"""SELECT MAX({idColumnName}) + 1 FROM {tableName};""")

    return cursor.fetchone()[0]

def startSession(uid, sessionNo):
    cursor.execute(
        f"""INSERT into sessions VALUES ("{uid}", "{sessionNo}", {time.strftime("%Y-%m-%d")}, NULL);""")
    
    connection.commit()

    return

def endSession(uid):
    cursor.execute(
        f"""UPDATE sessions SET end={time.strftime("%Y-%m-%d")} WHERE uid="{uid}" AND end IS NULL;""")
    
    connection.commit()

    return

### INITAL FUNCTIONS ###
def createTables():
    global connection, cursor
    cursor.executescript("""drop table if exists perform;
drop table if exists artists;
drop table if exists plinclude;
drop table if exists playlists;
drop table if exists listen;
drop table if exists sessions;
drop table if exists songs;
drop table if exists users;

PRAGMA foreign_keys = ON;

create table users (
  uid		char(4),
  name		text,
  pwd		text,
  primary key (uid)
);
create table songs (
  sid		int,
  title		text,
  duration	int,
  primary key (sid)
);
create table sessions (
  uid		char(4),
  sno		int,
  start 	date,
  end 		date,
  primary key (uid,sno),
  foreign key (uid) references users
	on delete cascade
);
create table listen (
  uid		char(4),
  sno		int,
  sid		int,
  cnt		real,
  primary key (uid,sno,sid),
  foreign key (uid,sno) references sessions,
  foreign key (sid) references songs
);
create table playlists (
  pid		int,
  title		text,
  uid		char(4),
  primary key (pid),
  foreign key (uid) references users
);
create table plinclude (
  pid		int,
  sid		int,
  sorder	int,
  primary key (pid,sid),
  foreign key (pid) references playlists,
  foreign key (sid) references songs
);
create table artists (
  aid		char(4),
  name		text,
  nationality	text,
  pwd		text,
  primary key (aid)
);
create table perform (
  aid		char(4),
  sid		int,
  primary key (aid,sid),
  foreign key (aid) references artists,
  foreign key (sid) references songs
);
""")


def insert_data():
    global connection, cursor
    cursor.executescript("""PRAGMA foreign_keys = ON;

insert into users values ('u1',"Scott G", "1234");
insert into users values ('u10',"Davood Rafiei", "1234");
insert into users values ('u20',"Hamed Mirzaei", "1234");

insert into songs values (5, "Wavinflag", 220);
insert into songs values (10, "Nice for what", 210);
insert into songs values (11, "Hold on, we are going home", 227);

insert into sessions values ("u10", 1, "2022-09-27", "2022-09-28");
insert into sessions values ("u20", 1, "2022-09-25", "2022-09-27");

insert into listen values ("u10", 1, 5, 1.2);
insert into listen values ("u10", 1, 11, 2.0);

insert into playlists values (30, "Songs for 291", "u10");

insert into plinclude values (30, 10, 1);
insert into plinclude values (30, 11, 2);
insert into plinclude values (30, 5, 3);

insert into artists values ("a10", "Drake", "Canada", "1234");
insert into artists values ("a20", "Bob Ezrin", "Canadian", "1234");

insert into perform values ("a10", 5);
insert into perform values ("a20", 10);
insert into perform values ("a20", 11);""")
    connection.commit()
    return
