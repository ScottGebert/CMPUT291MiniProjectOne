

-- INSERT into artists Values ('u1', "Scott", "Canada", "1234");

-- SELECT * FROM USERS;


SELECT count(*) FROM songs where Lower(title)='wavinflag' AND duration=220;


select * From songs INNER JOIN perform on songs.sid = perform.sid;