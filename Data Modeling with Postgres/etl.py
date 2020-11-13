import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - Reads song files from filepath 
    - Extracts assigned values from the file and stores them into song and artist tables
    
    """
    
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_col = ['song_id', 'title', 'artist_id', 'year', 'duration']
    song_data = list(df[song_col].values.flatten())   
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_col = ['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']
    artist_data = list(df[artist_col].values.flatten())
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - Reads log file from filepath
    - Creates dimensional tables and loads data on each table
    
    """
    
    # open log file
    df = pd.read_json(filepath, lines = True)
  
    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = ([t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday])
    column_labels = (['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']) 
    time_df = pd.DataFrame(index = t.index)
    time_df[column_labels[0]]=time_data[0]
    time_df[column_labels[1]]=time_data[1]
    time_df[column_labels[2]]=time_data[2]
    time_df[column_labels[3]]=time_data[3]
    time_df[column_labels[4]]=time_data[4]
    time_df[column_labels[5]]=time_data[5]
    time_df[column_labels[6]]=time_data[6]
    
    time_df = time_df.drop_duplicates()
    
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df = user_df.loc[user_df['userId'].notnull()]
    user_df = user_df.drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

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
        start_time = pd.Timestamp(row.ts, unit='ms')
        songplay_data = (index, start_time, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - Conducts file reading process from filepath
    - Displays number of files processed with matched data
    
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
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
    """
    - Driver function to connect with the entire process 
    
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
