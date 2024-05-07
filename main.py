import os
import json
from datetime import datetime
from get_access_token import check_expiry_time

def check_token_exist():
    # Check if the JSON file exists in the current directory
    if not os.path.exists('token.json'):
        # Create a new JSON object with today's date and time as a key
        data = {'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'credential': None}
        # Write the JSON data to the file
        with open('token.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f'Token JSON file not found. Creating a JSON with timestamp and access token: "token.json"')
        print('Obtaining a new access token credential.\n')


    else:
        print(f'JSON file already exists: "token.json". Checking last updated time')
        
        check_expiry_time()


# TODO: Add function to process the TSV into intermediate file.
# TODO: Add function to search tracks on Spotify
# TODO: Add function to add tracks to Spotify playlist

if __name__ == '__main__':
    print('Running Apple 2 Spotify Program.')
    check_token_exist()