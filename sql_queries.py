# Fact Table
# songplays - records in log data associated with song plays i.e. records with page NextSong
# songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
# Dimension Tables
# users - users in the app
# user_id, first_name, last_name, gender, level
# songs - songs in music database
# song_id, title, artist_id, year, duration
# artists - artists in music database
# artist_id, name, location, latitude, longitude
# time - timestamps of records in songplays broken down into specific units
# start_time, hour, day, week, month, year, weekday


# DROP TABLES

songplay_table_drop = "DROP TABLE songplays;"
user_table_drop = "DROP TABLE users"
song_table_drop = "DROP TABLE songs"
artist_table_drop = "DROP TABLE artists"
time_table_drop = "DROP TABLE time"

# CREATE TABLES

songplay_table_create = """
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id int PRIMARY KEY,
        start_time timestamp,
        user_id int,
        level int,
        song_id int,
        artist_id int,
        session_id int,
        location varchar,
        user_agent varchar
    )
"""

user_table_create = """
"""

song_table_create = """
"""

artist_table_create = """
"""

time_table_create = """
"""

# INSERT RECORDS

songplay_table_insert = """
"""

user_table_insert = """
"""

song_table_insert = """
"""

artist_table_insert = """
"""


time_table_insert = """
"""

# FIND SONGS

song_select = """
"""

# QUERY LISTS

create_table_queries = [
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]