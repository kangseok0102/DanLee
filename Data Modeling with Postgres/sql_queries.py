# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"



# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay (
                            songplay_id serial primary key, 
                            start_time timestamp, 
                            user_id int, 
                            level varchar, 
                            song_id varchar, 
                            artist_id varchar, 
                            session_id int, 
                            location varchar,
                            user_agent varchar);
                            """)

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
                            user_id int primary key,
                            first_name varchar(64),
                            last_name varchar(64),
                            gender char(1),
                            level varchar(32));
                            """)


song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (
                            song_id varchar primary key,
                            title varchar,
                            artist_id varchar,
                            year int,
                            duration numeric
                            );
                            """)

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist (
                            artist_id varchar primary key,
                            name varchar,
                            location varchar,
                            latitude numeric,
                            longitude numeric);
                            """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
                            start_time TIMESTAMP primary key,
                            hour int,
                            day int,
                            week int,
                            month int,
                            year int,
                            weekday int);
                            """)

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplay (
                            songplay_id,
                            start_time, 
                            user_id, 
                            level, 
                            song_id, 
                            artist_id, 
                            session_id, 
                            location,
                            user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (songplay_id) DO NOTHING;
                            """)

user_table_insert = ("""INSERT INTO users (
                            user_id,
                            first_name,
                            last_name,
                            gender,
                            level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
                            """)

song_table_insert = ("""INSERT INTO songs (
                            song_id,
                            title,
                            artist_id,
                            year,
                            duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO NOTHING;
                            """)

artist_table_insert = ("""INSERT INTO artist (
                            artist_id,
                            name,
                            location,
                            latitude,
                            longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO NOTHING;
                            """)


time_table_insert = ("""INSERT INTO time (
                            start_time,
                            hour,
                            day,
                            week,
                            month,
                            year,
                            weekday) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (start_time) DO NOTHING;
                            """)



# FIND SONGS

song_select = ("""SELECT song_id, artist.artist_id FROM songs JOIN artist ON songs.artist_id = artist.artist_id
                  WHERE songs.title = %s
                  AND artist.name = %s
                  AND songs.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
