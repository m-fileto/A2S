import os

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
        if strFileName in filename:
            print(f"{filename} found in the PlaylistsInfo directory")
            return
    print(f"\n[ERROR] {strFileName} NOT found in the PlaylistsInfo directory! Please make sure the file exists in the directory or check spelling of file name.")