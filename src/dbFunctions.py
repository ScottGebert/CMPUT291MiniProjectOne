from datetime import datetime
import sqlite3
import time

connection = None
cursor = None


### LOGIN FUNCTIONS ###
# Returns the userType if login is sucsessful otherwise returns None
def attemptLoginBothTables(id, pwd):
    userType = None
    if (loginUser(id, pwd)):
        userType = "user"
    elif (loginArtist(id, pwd)):
        userType = "artist"

    return userType


# Check if passed in id is in both users and artists
def idInBoth(id):
    cursor.execute(f"""SELECT uid as id FROM users WHERE LOWER(uid)='{id.lower()}'
                        UNION ALL
                        SELECT aid as id FROM artists WHERE LOWER(aid)='{id.lower()}';""")

    rows = cursor.fetchall()
    return True if len(rows) > 1 else False


# Returns True if login is sucsessful
def loginUser(id, pwd):
    cursor.execute(f"""SELECT * FROM users WHERE LOWER(uid)='{id.lower()}' and pwd='{pwd}'""")
    row = cursor.fetchone()
    return (False if row == None else True)


# Returns True if login is sucsessful
def loginArtist(id, pwd):
    cursor.execute(
        f"""SELECT * FROM artists WHERE LOWER(aid)='{id.lower()}' and pwd='{pwd}'""")
    row = cursor.fetchone()
    return (False if row == None else True)


# User ID can match aid so only check Users
def checkUserId(id):
    cursor.execute(f"""SELECT * FROM users WHERE LOWER(uid)='{id.lower()}'""")
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
        where LOWER(perform.aid)='{aid.lower()}' and Lower(songs.title)='{songName.lower()}' AND songs.duration={songDuration};""")

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


def getTopPlaylists(aid):
    cursor.execute(f"""SELECT  title, Count(*) as sCount FROM plinclude INNER JOIN perform on perform.sid = plinclude.sid 
    INNER JOIN playlists on playlists.pid = plinclude.pid
    WHERE LOWER(perform.aid)='{aid.lower()}'
    GROUP BY plinclude.pid
    ORDER BY sCount DESC
    LIMIT 3;
""")
    return cursor.fetchall()


def getTopUsers(aid):
    cursor.execute(f"""SELECT users.name, SUM(listen.cnt * songs.duration) as lTime FROM listen 
    INNER JOIN perform on listen.sid = perform.sid
    INNER JOIN songs on songs.sid = perform.sid
    INNER JOIN users on listen.uid = users.uid
    WHERE LOWER(perform.aid)='{aid.lower()}'
    GROUP BY listen.uid
    ORDER BY lTime  DESC
    LIMIT 3;
""")

    return cursor.fetchall()

### ALL FUNCTIONS ###
# Only works if the PK is an int
def getNextUnusedId(tableName, idColumnName):
    cursor.execute(
        f"""SELECT MAX({idColumnName}) + 1 FROM {tableName};""")

    return cursor.fetchone()[0]


## USERE FUNCTIONS ##
def getActiveSession(uid):
    cursor.execute(
        f"""SELECT sno FROM sessions WHERE uid="{uid}" AND sessions.end IS NULL;""")
    row = cursor.fetchone()
    if row != None:
        return row[0]

    return row

# starts a session for a user if one is not already started
def startSession(uid):
    # see if there is an active session
    sno = getActiveSession(uid)
    if sno == None:
        # if no active session, create a new one
        sno = getNextUnusedId('sessions', 'sno')
        if sno == None:
            sno = 1

        cursor.execute(
            f"""INSERT into sessions VALUES ("{uid}", "{sno}", "{datetime.now().strftime('%Y-%m-%d')}", NULL);""")

        connection.commit()
        print("Session started")

    return sno

# ends a session for a user
def endSession(uid):
    cursor.execute(
        f"""UPDATE sessions SET end="{datetime.now().strftime('%Y-%m-%d')}" WHERE uid="{uid}" AND sessions.end IS NULL AND start IS NOT NULL;""")

    connection.commit()

    return

# searches for songs & playlists given a list of keywords
# keywords are cross referenced with song titles and playlists they exist in
# results are ordered by number of matches
def searchSongsAndPlaylists(keywords):
    songQuery = f"""SELECT sid, title, duration FROM songs WHERE title LIKE '%{keywords[0]}%'\n"""
    playlistQuery = f"""SELECT pid AS id, pl.title, ifnull(cnt, 0) AS duration
		FROM (SELECT pid, playlists.title, SUM(duration) AS cnt FROM playlists LEFT OUTER JOIN plinclude USING(pid) LEFT OUTER JOIN songs USING(sid) GROUP BY pid) AS pl
		WHERE pl.title LIKE '%{keywords[0]}%'\n"""

    for i in range(1, len(keywords)):
        songQuery += "UNION ALL\n"
        songQuery += f"""SELECT sid, title, duration FROM songs WHERE title LIKE '%{keywords[i]}%'\n"""

        playlistQuery += "UNION ALL\n"
        playlistQuery += f"""SELECT pid AS id, pl.title, ifnull(cnt, 0) AS duration
		FROM (SELECT pid, playlists.title, SUM(duration) AS cnt FROM playlists LEFT OUTER JOIN plinclude USING(pid) LEFT OUTER JOIN songs USING(sid) GROUP BY pid) AS pl
		WHERE pl.title LIKE '%{keywords[i]}%'\n"""

    cursor.execute(
        f"""SELECT id, title, duration, type
            FROM (
                SELECT sid AS id, title, duration AS duration, 'Song' AS type, count(*) AS matches
                FROM ({songQuery})
                GROUP BY id
                UNION
                SELECT id, title, duration, 'Playlist' AS type, count(*) AS matches
                FROM ({playlistQuery})
                GROUP BY id
                )
            ORDER BY matches DESC;""")

    return cursor.fetchall()

# adds an entry to listen table if user has not listened to this song during this session
# o.w. the cnt field is incremented
def listenToSong(uid, song):
    # if there is an active session, this function won't start a new one
    sno = startSession(uid)

    cursor.execute(
        f"""SELECT * FROM listen WHERE uid="{uid}" AND sno={sno} AND sid={song[0]};""")
    row = cursor.fetchone()
    if row == None:
        cursor.execute(
            f"""INSERT INTO listen VALUES ("{uid}", "{sno}", {song[0]}, 1);""")
    else:
        cursor.execute(
            f"""UPDATE listen SET cnt=cnt + 1 WHERE uid="{uid}" AND sno="{sno}" AND sid={song[0]};""")

    connection.commit()

# gets all artists that have performed a song
def getArtistsFromSong(sid):
    cursor.execute(
        f"""SELECT name FROM perform LEFT OUTER JOIN artists USING(aid) WHERE sid={sid};""")
    artists = [i[0] for i in cursor.fetchall()]
    return artists

# returns all playlists that a given song exists in
def getPlaylistsFromSong(sid):
    cursor.execute(
        f"""SELECT title FROM plinclude LEFT OUTER JOIN playlists USING(pid) WHERE sid={sid};""")
    playlists = [i[0] for i in cursor.fetchall()]
    return playlists

# returns all playlists owner by a user with given uid
def getPlaylistsFromUid(uid):
    cursor.execute(f"""SELECT pid, title FROM playlists WHERE uid="{uid}";""")
    return cursor.fetchall()

# creates a new playlist for a user with a given title
def createNewPlaylist(uid, title):
    pid = getNextUnusedId('playlists', 'pid')
    if pid == None:
        pid = 1

    cursor.execute(
        f"""INSERT INTO playlists VALUES ({pid}, "{title}", "{uid}");""")
    connection.commit()

    return pid

# adds a song to a playlist. Sort order is assigned to the bottom of the playlist
def addSongToPlaylist(sid, pid):
    if songExistsInPlaylist(sid, pid):
        print("Song already exists in playlist")
        return

    # get next sort order value
    cursor.execute(
        f"""SELECT MAX(sorder) FROM plinclude WHERE pid={pid} AND sid="{sid}";""")
    sorder = cursor.fetchone()[0]
    if sorder == None:
        sorder = 1
    else:
        sorder = sorder + 1

    cursor.execute(
        f"""INSERT INTO plinclude VALUES ({pid}, "{sid}", {sorder});""")
    connection.commit()

    return

# returns true if a song exists in a playlist
def songExistsInPlaylist(sid, pid):
    cursor.execute(
        f"""SELECT COUNT(*) FROM plinclude WHERE pid={pid} AND sid={sid}""")
    count = cursor.fetchone()
    return (True if count[0] > 0 else False)

# searches for artists given a list of keywords
# keywords are cross referenced with artist names and song titles
# results are ordered by number of matches
def searchArtists(keywords):
    nameQuery = f"""SELECT aid, name, nationality FROM artists WHERE name LIKE '%{keywords[0]}%'\n"""
    songQuery = f"""SELECT aid, name, nationality
                    FROM artists LEFT OUTER JOIN perform USING(aid) LEFT OUTER JOIN songs USING(sid) 
                    WHERE title LIKE '%{keywords[0]}%' 
                    GROUP BY aid
                    HAVING COUNT(*) > 0\n"""

    for i in range(1, len(keywords)):
        nameQuery += "UNION ALL\n"
        nameQuery += f"""SELECT aid, name, nationality FROM artists WHERE name LIKE '%{keywords[i]}%'\n"""

        songQuery += "UNION ALL\n"
        songQuery += f"""SELECT aid, name, nationality
                        FROM artists LEFT OUTER JOIN perform USING(aid) LEFT OUTER JOIN songs USING(sid) 
                        WHERE title LIKE '%{keywords[i]}%' 
                        GROUP BY aid
                        HAVING COUNT(*) > 0\n"""

    cursor.execute(
        f"""WITH artistSongCnt(aid, cnt) AS 
            (SELECT aid, COUNT(*)
             FROM perform
             GROUP BY aid
            )
            SELECT q.aid, name, nationality, artistSongCnt.cnt AS songcount
            FROM (
                SELECT aid, name, nationality, count(*) AS matches
                FROM ({nameQuery})
                GROUP BY aid
                UNION ALL
                SELECT aid, name, nationality, count(*) AS matches
                FROM ({songQuery})
                GROUP BY aid
                ) AS q, artistSongCnt
            WHERE q.aid=artistSongCnt.aid
            GROUP BY q.aid
            ORDER BY SUM(matches) DESC;""")

    return cursor.fetchall()

# gets all songs performed by an artist given their aid
def getArtistsSongs(aid):
    cursor.execute(
        f"""SELECT sid, title, duration FROM perform LEFT OUTER JOIN songs USING(sid) WHERE aid="{aid}";""")
    return cursor.fetchall()

# gets all songs that exist in a playlist given a pid
def getSongsInPlaylist(pid):
    cursor.execute(
        f"""SELECT sid, title, duration FROM plinclude LEFT OUTER JOIN songs USING(sid) WHERE pid={pid};""")
    return cursor.fetchall()


### INITAL FUNCTIONS ###
def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return cursor

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
insert into songs values (15, "Move bitch, get out the way", 223);
insert into songs values (16, "Nice for nothing", 230);
insert into songs values (18, "Home", 205);
insert into songs values (19, "song", 205);
insert into songs values (20, "another song", 205);

insert into sessions values ("u10", 1, "2022-09-27", "2022-09-28");
insert into sessions values ("u20", 1, "2022-09-25", "2022-09-27");

insert into listen values ("u10", 1, 5, 1.2);
insert into listen values ("u10", 1, 11, 2.0);

insert into playlists values (30, "Songs for 291", "u10");
insert into playlists values (32, "Scotts songs", "u1");
insert into playlists values (33, "Depressing songs", "u10");
insert into playlists values (34, "Don't know but it sucks", "u20");
insert into playlists values (35, "Another playlist", "u1");

insert into plinclude values (30, 10, 1);
insert into plinclude values (30, 11, 2);
insert into plinclude values (30, 5, 3);
insert into plinclude values (32, 11, 1);
insert into plinclude values (32, 15, 2);
insert into plinclude values (32, 16, 3);

insert into artists values ("a10", "Drake", "Canada", "1234");
insert into artists values ("a20", "Bob Ezrin", "Canadian", "1234");
insert into artists values ("a21", "Willie Nelson", "Canadian", "1234");
insert into artists values ("a22", "X", "Canadian", "1234");
insert into artists values ("a23", "AA", "Canadian", "1234");

insert into perform values ("a10", 5);
insert into perform values ("a10", 10);
insert into perform values ("a20", 10);
insert into perform values ("a20", 11);
insert into perform values ("a21", 11);
insert into perform values ("a22", 15);
insert into perform values ("a22", 16);
insert into perform values ("a23", 16);
insert into perform values ("a23", 18);
insert into perform values ("a23", 19);
insert into perform values ("a23", 20);""")
    connection.commit()
    return
