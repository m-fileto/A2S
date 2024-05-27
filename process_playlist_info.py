import os
from datetime import datetime
import json
import requests

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
            process_tsv_file(filename)
            return 
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
            strPlaylistName = tsv_file_name
            if strPlaylistName.endswith('.tsv'):
                strPlaylistName = strPlaylistName[:-4]
            json_file_name = f'{tsv_file_name}_{timestamp}.json'
            json_file_path = os.path.join(directory, json_file_name)
            with open(json_file_path, 'w') as f:
                json.dump(dictionary, f, indent=4)
            print(f'\n[INFO] Successfully created JSON file: {json_file_name}')
            return search_tracks_in_spotify(dictionary, tsv_file_name)
    print(f"\n[ERROR] {tsv_file_name} NOT found in the PlaylistsInfo directory! Please make sure the file exists in the directory or check spelling of file name.")

def search_tracks_in_spotify(dictPlaylistData, fileName):
    if not os.path.exists('token.json'):
        return print_error_exit_message_process_tsv('Authentication token.json not found. Please run option in menu to retreive acess token first.')
        
    strAccessToken = None
    with open('token.json', 'r') as f:
        dictJsonData = json.load(f)
        strAccessToken = dictJsonData['credential']
    
    if strAccessToken is None:
        return print_error_exit_message_process_tsv('Access token not found (none type). Please run option in menu to retreive acess token first.')
    elif strAccessToken.strip() == '':
        return print_error_exit_message_process_tsv('Access token not found (empty string). Please run option in menu to retreive acess token first.')

    # Spotify API endpoint for searching tracks
    url = 'https://api.spotify.com/v1/search'
    
    list_track_ids = []
    for key, val in dictPlaylistData.items():
        artist = key
        list_songs = val
        print(f'{artist} songs: {list_songs}')
        for song in list_songs:     
            # Parameters for the search query
            params = {
                'q': f'track:{song} artist:{artist}',
                'type': ['track']
            }
            
            # Authorization header with access token
            headers = {
                'Authorization': f'Bearer {strAccessToken}'
            }
            
            # Sending GET request to Spotify API
            response = requests.get(url, params=params, headers=headers)
            
            # Checking if request was successful
            if response.status_code == 200:
                # Extracting track information from the response
                track_data = response.json()['tracks']['items']
                if track_data:
                    # Extracting track ID from the first result
                    track_id = track_data[0]['id']
                    list_track_ids.append(track_id)
                
                # TODO: save to array songs not found
                else:
                    print(f'[*** MISSING SONG ***] Could not find a track id for artist "{artist}" for song name "{song}"')
            else:
                print(f'\n[ERROR] Failed to search for track "{song}" with artist "{artist}". Status code: {response.status_code}')
                if response.status_code == 401:
                    print(f'[ERROR] Access Token most likely expired!!! Run option to retreive access token.')
                return []
    
    # Save the track IDs into a JSON file
    if len(list_track_ids) == 0:
        return print('\n[INFO] No track IDs found. Returning to menu.')
    else:
        strPlaylistName = fileName
        if strPlaylistName.endswith('.tsv'):
            strPlaylistName = strPlaylistName[:-4]

        strDate = datetime.now().strftime('%Y-%m-%d')
        strTimestamp = datetime.now().strftime('%H-%M-%S')
        strJsonFilename = f'tracks_{strPlaylistName}_{strDate}_{strTimestamp}.json'
        dictJsonData = {'track_ids': list_track_ids}
       
       # TODO: save to some other path to not bloat directory?
        with open(os.path.join('PlaylistsInfo', strJsonFilename), 'w') as f:
            json.dump(dictJsonData, f, indent=4)
       
        print(f'\n[INFO] Saved track IDs into JSON file: "{strJsonFilename}"')

        # TODO: create new helper for adding to playlist now.