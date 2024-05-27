import os
from datetime import datetime
import json
import requests

def print_error_exit_message_process_tsv(errMsg):
    print('\n\n\t\tExiting Program due to ERROR. Msg: {errMsg}...\n\n')
    exit()

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
    print('Be sure to examine the column number for Artist name since albums tend to be the name of the artist. This will cause downstream errors/not found in spotify query search!')
    artist_column = input(f"\nEnter the column number from the array example above that indicates ARTIST name in the {tsv_file_name} file: ")
    track_column = input(f"Enter the column number from the array example above that indicates TRACK name in the {tsv_file_name} file: ")

    while not artist_column.isdigit() or not track_column.isdigit():
        print('\n[ERROR] Please enter a valid column number.')
        artist_column = input(f"\nEnter the column number from the array example above that indicates ARTIST name in the {tsv_file_name} file: ")
        track_column = input(f"Enter the column number from the array example above that indicates TRACK name in the {tsv_file_name} file: ")

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

            print(f'\n[INFO] Successfully generated dictionary of artist to track names')
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
        dictJsonData = {'track_ids': list_track_ids}
        add_tracks_to_playlist(dictJsonData)

def split_array_into_chunks(array, chunk_size):
    chunks = []
    for i in range(0, len(array), chunk_size):
        chunks.append(array[i:i + chunk_size])
    return chunks

# This does NOT currently check for duplicates. Nice to have feature.
def add_tracks_to_playlist(dictTrackData):
    
    # Load JSON data from file
    jsonTokenData = None
    with open('token.json') as f:
        jsonTokenData = json.load(f)

    accessToken: str = jsonTokenData['credential']
    listTrackIds: list[str] = dictTrackData['track_ids']
    playlistId = input(f'\nEnter the playlist ID on spotify (i.e. found in Browser URL after /playlist/):\n')
    if playlistId.strip() == '':
        return print_error_exit_message_process_tsv('Not a valid playlist id with empty string')    
    
    passedCheckPlyalist = check_tracks_already_in_playlist(playlistId, accessToken, listTrackIds)
    if passedCheckPlyalist == False or passedCheckPlyalist == None:
        return print_error_exit_message_process_tsv('Did not pass check for tracks already in playlist')
    elif len(listTrackIds) == 0:
        return print('\n[INFO] List of track IDs is empty after removing/checking for duplicates. Returning to menu.')

    print('\n[INFO] Adding tracks to playlist...')
    # Spotify API endpoint for adding to tracks (using POST HTTP Method)
    url = f'https://api.spotify.com/v1/playlists/{playlistId}/tracks'

    chunkApiReqs = split_array_into_chunks(listTrackIds, 100)
    print(f'\n[INFO] There will be {len(chunkApiReqs)} requests made to add the chunked tracks to the playlist.\n')
    for listChunkedTracks in chunkApiReqs:
            listUriTracks = []
            for trackId in listChunkedTracks:
                uriFormat = 'spotify:track:' + trackId
                listUriTracks.append(uriFormat)

            # Authorization header with access token
            headers = {
                    'Authorization': f'Bearer {accessToken}',
                    'Content-Type': 'application/json'
            }
            data = {
                'uris': listUriTracks
            }
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
            
            # Checking if request was successful
            if response.status_code >= 200 and response.status_code < 300:
                index = listChunkedTracks.index(trackId)
                if index < len(listChunkedTracks) - 1:
                    print(f"[INFO] Tracks added to playlist successfully. {len(listChunkedTracks) - index - 1} chunks left.")
                else:
                    print("[INFO] Tracks added to playlist successfully. This is the last chunk now returning to the main menu.")
            else:
                return print_error_exit_message_process_tsv('Failed to add tracks to playlist. Status code: ' + str(response.status_code) + '. Message:"' + response.message + '"')
            
def check_tracks_already_in_playlist(idPlaylist, accessToken,listTracks):
    
    print('\n[INFO] Checking if tracks already exist in playlist\n')

    # Spotify API endpoint for search tracks in playlist (using GET HTTP Method)
    url = f'https://api.spotify.com/v1/playlists/{idPlaylist}/tracks'
    # Authorization header with access token
    headers = { 'Authorization': f'Bearer {accessToken}'}

    response = requests.get(url=url, headers=headers)
    if response.status_code >= 200 and response.status_code < 300:
        listPlaylistTracks = response.json()['items']
        for track in listPlaylistTracks:
            if track['track']['id'] in listTracks:
                print(f'[INFO] Track "{track["track"]["name"]}" by artist: "{track["track"]["artists"][0]["name"]}" already in playlist. Removing track from request data structure.')
                listTracks.remove(track['track']['id'])
    else:
        print(f'[ERROR] Failed to get tracks in playlist. Status code: "{response.status_code}"')
        return False

    return True