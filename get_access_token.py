import os
import json
from datetime import datetime, timedelta
import requests
import json
from urllib.parse import urlencode


# Spotify access tokens are only valid for 1 hour session
def check_expiry_time():
    
    # Check if the JSON file exists in the current directory
    if not os.path.exists('token.json'):
        print('\nERROR! Could not find "token.json" after program initialization. Please rerun program.')
    else:
        # Read existing data from the file
        jsonData = None
        with open('token.json', 'r') as f:
            jsonData = json.load(f)

        lastUpdatedTimeStamp = jsonData['last_updated']
        hasHourPassed = bool_hour_passed(lastUpdatedTimeStamp)
        if hasHourPassed == True:
            fetch_token_credential()
        elif jsonData['credential'] is None:
            fetch_token_credential()
        else:
            timeUpdated = datetime.strptime(lastUpdatedTimeStamp, '%Y-%m-%d %H:%M:%S')
            timeRightNow = datetime.now()

            # Calculate an hour from the given timestamp
            futureHourTime = timeUpdated + timedelta(hours=1)

            # Calculate the time difference between the future time and the current time
            timeDifference = futureHourTime - timeRightNow
            minutesLeft = int(timeDifference.total_seconds() // 60)

            print(f'Credential Token still valid. Remaining minutes until token expires: {minutesLeft}\n')

def bool_hour_passed(timestamp):
    # Convert the timestamp string to a datetime object
    timestamp_datetime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    
    # Get the current time
    current_time = datetime.now()
    
    # Calculate the difference between the current time and the timestamp
    time_difference = current_time - timestamp_datetime

    # Check if the difference is greater than or equal to 60 minutes
    return time_difference >= timedelta(minutes=60)

def fetch_token_credential():
    # Spotify API endpoint for authorization
    authorization_base_url = 'https://accounts.spotify.com/authorize'

    # Your application's client ID and client secret
    client_id = input('Enter the Client ID from the Spotify Developer App: ')
    client_secret = input('Enter the Client Secret from the Spotify Developer App: ')

    # Define the scopes your application requires
    scopes = ['playlist-modify-public', 'playlist-modify-private']

    # Redirect URI for your application (must be registered in your Spotify Developer Dashboard)
    redirect_uri = 'https://localhost'

    # Construct the authorization URL with the required parameters
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes),
        'response_type': 'code'
    }
    authorization_url = authorization_base_url + '?' + urlencode(params)

    # Open the authorization URL in a browser to allow the user to authenticate and authorize your application
    print("\nPlease go to the following URL and authorize access:\n")
    print(authorization_url)

    # After the user authorizes your application, they will be redirected to your redirect URI with an authorization code
    authorization_code = input("\nEnter the authorization code from the callback URL (found on the ?code URL param):\n")

    # Exchange the authorization code for an access token
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(token_url, data=token_data)


    # TODO: Return early when invalid response returned

    # Extract the access token from the response
    access_token = response.json().get('access_token')

    # Now you can use the access token to make requests to the Spotify API with the specified scopes
    print("Valid Access token credential:\n", access_token)

    # TODO: write the credential to the json token

    # with open('token.json', 'w') as file:
    #     data = {'access_token': access_token}

    #     json.dump(data, file)