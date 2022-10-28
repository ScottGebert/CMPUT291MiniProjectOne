

-- INSERT into artists Values ('u1', "Scott", "Canada", "1234");

-- SELECT * FROM USERS;


-- SELECT count(*) FROM songs where Lower(title)='wavinflag' AND duration=220;


-- select * From songs INNER JOIN perform on songs.sid = perform.sid;


-- SELECT * FROM users; 
 SELECT * FROM playlists;
-- SELECT * FROM plinclude;
 SELECT * FROM perform;

-- SELECT  title, Count(*) as sCount FROM plinclude INNER JOIN perform on perform.sid = plinclude.sid 
--     INNER JOIN playlists on playlists.pid = plinclude.pid
--     WHERE perform.aid='a20'
--     GROUP BY plinclude.pid
--     ORDER BY sCount DESC
--     LIMIT 3;

--UPDATE playlists set title='Super duper playlist' WHERE pid = 32;
-- DELETE FROM plinclude WHERE sorder='u10';
--  INSERT INTO plinclude VALUES (31, 5, 'u10');
--  INSERT INTO plinclude VALUES (31,12 , 2);
--   INSERT INTO plinclude VALUES (32, 12, 1);
   --  INSERT INTO plinclude VALUES (33, 13, 1);
--  INSERT INTO plinclude VALUES (33, 10, 3);
--INSERT INTO playlists VALUES (33, "top p test", 'u10');
-- INSERT INTO playlists VALUES (32, 'top playlist test', 'u10');
