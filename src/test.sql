

-- INSERT into artists Values ('u1', "Scott", "Canada", "1234");

-- SELECT * FROM USERS;


-- SELECT count(*) FROM songs where Lower(title)='wavinflag' AND duration=220;


-- select * From songs INNER JOIN perform on songs.sid = perform.sid;


-- SELECT * FROM users; 
 SELECT * FROM playlists;
SELECT * FROM plinclude;
 SELECT * FROM perform;
 --SELECT * FROM sessions;
 -- SELECT * FROM listen;

-- SELECT users.name, SUM(listen.cnt * songs.duration) as lTime FROM listen 
--     INNER JOIN perform on listen.sid = perform.sid
--     INNER JOIN songs on songs.sid = perform.sid
--     INNER JOIN users on listen.uid = users.uid
--     WHERE perform.aid='a10'
--     GROUP BY listen.uid
--     ORDER BY lTime  DESC
--     LIMIT 3;

SELECT  title, Count(*) as sCount FROM plinclude INNER JOIN perform on perform.sid = plinclude.sid 
    INNER JOIN playlists on playlists.pid = plinclude.pid
    WHERE perform.aid='a10'
    GROUP BY plinclude.pid
    ORDER BY sCount DESC
    LIMIT 3;

--  INSERT INTO listen VALUES ('u20', 1, 12, 3);
-- INSERT INTO listen VALUES ('u20', 1, 13, 2.2);
--UPDATE playlists set title='Super duper playlist' WHERE pid = 32;
-- DELETE FROM plinclude WHERE sorder='u10';
--  INSERT INTO plinclude VALUES (31, 5, 'u10');
--  INSERT INTO plinclude VALUES (31,12 , 2);
--   INSERT INTO plinclude VALUES (32, 12, 1);
   --  INSERT INTO plinclude VALUES (33, 13, 1);
--  INSERT INTO plinclude VALUES (33, 10, 3);
--INSERT INTO playlists VALUES (33, "top p test", 'u10');
-- INSERT INTO playlists VALUES (32, 'top playlist test', 'u10');
