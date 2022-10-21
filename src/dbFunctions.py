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
    return


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

insert into users values ("u10","Davood Rafiei", "1234");
insert into users values ("u20","Hamed Mirzaei", "1234");

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