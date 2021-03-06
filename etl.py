import os
import glob
import psycopg2
import pandas as pd
from sql_queries import (
    artist_table_insert,
    user_table_insert,
    songplay_table_insert,
    time_table_insert,
    song_select,
    song_table_insert,
)


def process_song_file(cur, filepath):
    """
    This function reads song data from a json file and insert on sparkifydb database.


    Parameters
    ----------
    cur : object
        Sparkifydb cursor.
    filepath : str
        Path to JSON song file.
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(df[["song_id", "title", "artist_id", "year", "duration"]].values[0])
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = list(
        df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0]
    )
    try:
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as e:
        print(e)


def process_log_file(cur, filepath):
    """
    This function reads log data from a json file, transform and insert on sparkifydb database.


    Parameters
    ----------
    cur : object
        Sparkifydb cursor.
    filepath : str
        Path to JSON song file.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit='ms')
    df["ts"] = t

    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ["timestamp", "hour", "day", "week", "month", "year", "weekday"]
    time_df = pd.DataFrame({key: value for (key, value) in zip(column_labels, time_data)})

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e:
            print(e)

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as e:
            print(e)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except psycopg2.Error as e:
            print(e)


def process_data(cur, conn, filepath, func):
    """
    This function iterates over log and song files, process data and insert on sparkifydb database.


    Parameters
    ----------
    cur : object
        Sparkifydb cursor.
    conn : object
        Conection to sparkifydb database.
    filepath : str
        Path to data directory.
    func : function
        Function that process the data (process_song_file or process_log_file)
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
