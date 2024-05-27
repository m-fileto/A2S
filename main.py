import os
import json
import sys
from datetime import datetime
import argparse
from get_access_token import check_expiry_time, fetch_token_credential
from process_playlist_info import search_playlists_info

# Record the output stream for inspection
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
    def flush(self):
        for f in self.files:
            f.flush()

def create_json_client_info():
    if not os.path.exists('client.json'):
        print('[INFO] Did not find "client.json". Creating client info json for future requests.')
        dictClientData = {'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'client_id': None,
                'client_secret': None}

        # Your application's client ID and client secret
        strClientId = input('\nEnter the Client ID from the Spotify Developer App:\n')
        while strClientId.strip() == '':
            strClientId = input('[ERROR] Empty Client ID. Enter a non empty Client ID from the Spotify Developer App:\n')

        strClientSecret = input('\nEnter the Client Secret from the Spotify Developer App:\n')
        while strClientSecret.strip() == '':
            strClientSecret = input('[ERROR] Empty Client Secret. Enter a non empty Client Secret from the Spotify Developer App:\n')

        dictClientData['client_id'] = strClientId
        dictClientData['client_secret'] = strClientSecret
        with open('client.json', 'w') as file:
            json.dump(dictClientData, file, indent=4)

        print('[SUCCESS] Successfully created "client.json"\n')
    else:
        print('[INFO] "client.json" already exists. Step not required anymore.\n')

def check_token_exist():
    # Check if the JSON file exists in the current directory
    if not os.path.exists('token.json'):
        # Create a new JSON object with today's date and time (YYYY-MM-DD HH24:MI:SS) as a key
        dictJsonData = {'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'credential': None}
        # Write the JSON data to the file
        with open('token.json', 'w') as f:
            json.dump(dictJsonData, f, indent=4)
        
        print(f'[INFO] Token JSON file not found. Creating a JSON with timestamp and access token: "token.json"')
        print('[INFO] Obtaining a new access token credential.\n')

        fetch_token_credential(dictJsonData)

    else:
        print(f'[INFO] JSON file already exists: "token.json". Checking last updated time')
        check_expiry_time()

def user_interaction_menu():

    # Disclaimer info
    print('\nBefore running the program, please make sure you have met the following requirements:')
    print('1. You have a Spotify account created')
    print('2. You have a Spotify Developer account created and an app setup with the proper configuration')
    print('3. You are currently logged into Spotify on your web browser running this script.')
    print('4. You have a TSV of your desired playlist saved into the "PlaylistsInfo" directory of this program.')
    print('5. You have a playlist created in Spotify to add tracks.')
    print('\nIf you DO NOT meet any of these requirements, please refer to the README.md file for more information before attempting.\n')

    strAcknowledge = input("\nDid you acknowledge the disclaimer above? (yes/no): ")
    while (strAcknowledge.lower().strip() != 'yes' and strAcknowledge.lower().strip() != 'no'):
        strAcknowledge = input('\n[WARNING] Invalid input. Did you acknowledge the disclaimer? (yes/no): ')
    if strAcknowledge.lower().strip() != 'yes':
        return print('\n[ERROR] User must acknowledge disclaimer before attempting.\n')

    while True:
        print("""
        MENU:
        1. Run program end to end (steps 2 to 4)
        2. Create JSON client info
        3. Token Authentication Check
        4. Process playlist info and add to Spotify Playlist
        q. Quit Program
        """)
        user_input = input("Enter a number from the menu or 'q' to exit: ")
        print('\n')
        if user_input == '1':
            create_json_client_info()
            check_token_exist()
            search_playlists_info()
        elif user_input == '2':
            create_json_client_info()
        elif user_input == '3':
            check_token_exist()
        elif user_input == '4':
            search_playlists_info()
        elif user_input == 'q':
            print('[INFO] Program exited.\n')
            break
        else:
            print('\n[ERROR] Invalid input. Please rerun script and enter a number from the menu or "q" to exit.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script to convert Apple Music playlists to Spotify.')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    if args.debug:
        # Save a copy of the original standard output
        original_stdout = sys.stdout

        # Create a log file and redirect standard output to it
        date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = open(os.path.join('Logs', f'log_{date_str}.txt'), 'w')
        sys.stdout = Tee(sys.stdout, log_file)

    print('\n\t\tRunning Apple 2 Spotify Program.\n')
    
    user_interaction_menu()

    if args.debug:
        # Close the log file and restore the original standard output
        log_file.close()
        sys.stdout = original_stdout