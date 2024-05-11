import os
import json
from datetime import datetime
from get_access_token import check_expiry_time, fetch_token_credential

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


# TODO: Add ability to update client.json either ID or secret
# TODO: Add function to process the TSV into intermediate file.
# TODO: Add function to search tracks on Spotify
# TODO: Add function to add tracks to Spotify playlist

if __name__ == '__main__':
    print('\n\t\tRunning Apple 2 Spotify Program.\n')
    
    create_json_client_info()
    check_token_exist()