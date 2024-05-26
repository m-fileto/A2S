import os
from datetime import datetime
import json

def print_error_exit_message_process_tsv(errMsg):
    print('\n\n\t\tExiting Program due to ERROR. Msg: {errMsg}...\n\n')

def search_playlists_info():
    strFileName = input("Enter the playlsist file name (e.g. MyPlaylist.tsv or MyPlaylist): ")
    while (strFileName.strip() == ''):
        strFileName = input('\n[WARNING] Empty directory path. Enter a non empty directory path: ')
    
    if not strFileName.endswith('.tsv'):
        strFileName += '.tsv'

    directory = 'PlaylistsInfo'
    for filename in os.listdir(directory):
        if strFileName == filename:
            print(f"[INFO] {filename} found in the PlaylistsInfo directory")
            return process_tsv_file(filename)
    print(f"\n[ERROR] {strFileName} NOT found in the PlaylistsInfo directory! Please make sure the file exists in the directory or check spelling of file name.")


def process_tsv_file(tsv_file_name):

    directory = 'PlaylistsInfo'
    for filename in os.listdir(directory):
        if tsv_file_name == filename:
            tsv_file_path = os.path.join(directory, filename)
            with open(tsv_file_path, 'r') as f:
                first_line = f.readline()
                first_line_array = first_line.split('\t')
                print(f"[INFO] TSV array structure for {tsv_file_name}")
                print(f'\n[Array -->]: {first_line_array}')

    print('\n^^^^ With the array above indicate the column numbers of the artist name and track name in the TSV file (Index starts at 1).')
    print('\nBe sure to examine the column number for Artist name since albums tend to be the name of the artist. This will cause downstream errors/not found in spotify query search!')
    artist_column = input(f"\nEnter the column number that indicates ARTIST name in the {tsv_file_name} file: ")
    track_column = input(f"\nEnter the column number that indicates TRACK name in the {tsv_file_name} file: ")

    while not artist_column.isdigit() or not track_column.isdigit():
        print('\n[ERROR] Please enter a valid column number.')
        artist_column = input(f"\nEnter the column number that indicates ARTIST name in the {tsv_file_name} file: ")
        track_column = input(f"\nEnter the column number that indicates TRACK name in the {tsv_file_name} file: ")

    # Assumes that index number starts with 1 
    artist_column = int(artist_column) - 1
    track_column = int(track_column) - 1

    dictionary = {}
    directory = 'PlaylistsInfo'
    for filename in os.listdir(directory):
        if tsv_file_name == filename:
            tsv_file_path = os.path.join(directory, filename)
            with open(tsv_file_path, 'r') as f:
                for line in f:
                    line = line.strip().split('\t')
                    print(line)
                    if line:
                        artist_name = line[artist_column]
                        track_name = line[track_column]
                        if artist_name not in dictionary:
                            dictionary[artist_name] = [track_name]
                        else:
                            dictionary[artist_name].append(track_name)

            # Generate a timestamp string in format YYYY-MM-DD_HH-MM-SS
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            # Add the timestamp to the filename
            json_file_name = f'{tsv_file_name}_{timestamp}.json'
            json_file_path = os.path.join(directory, json_file_name)
            with open(json_file_path, 'w') as f:
                json.dump(dictionary, f, indent=4)
            print(f'\n[INFO] Successfully created JSON file: {json_file_name}')
            return
    print(f"\n[ERROR] {tsv_file_name} NOT found in the PlaylistsInfo directory! Please make sure the file exists in the directory or check spelling of file name.")