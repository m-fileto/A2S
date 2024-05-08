import os
from datetime import datetime, timedelta
import requests
import json
from urllib.parse import urlencode


def print_error_exit_message():
    print('\n\n\t\tExiting Program due to ERROR...\n\n')

# Spotify access tokens are only valid for 1 hour session
def check_expiry_time():
    
    # Check if the JSON file exists in the current directory
    if not os.path.exists('token.json'):
        print('\n[ERROR] Could not find "token.json" after program initialization. Please rerun program.')
        print_error_exit_message()
    else:
        # Read existing data from the file
        jsonData = None
        with open('token.json', 'r') as f:
            jsonData = json.load(f)

        lastUpdatedTimeStamp = jsonData['last_updated']
        hasHourPassed = bool_hour_passed(lastUpdatedTimeStamp)
        if hasHourPassed == True:
            print('[WARN] More than 1 hour has passed! A new authorization token will be requested with your input.')
            fetch_token_credential()
        elif jsonData['credential'] is None:
            print('[INFO] Fetching valid token credential since this is null. (Most likely due to first time program execution)')
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
    objDatetimeArg = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    
    # Get the current time
    objCurrentDatetime = datetime.now()
    
    # Calculate the difference between the current time and the timestamp
    differenceTime = objCurrentDatetime - objDatetimeArg

    # Check if the difference is greater than or equal to 60 minutes
    return differenceTime >= timedelta(minutes=60)

def fetch_token_credential():
    # Spotify API endpoint for authorization
    STR_AUTHENTICATE_URL = 'https://accounts.spotify.com/authorize'

    # Your application's client ID and client secret
    strClientId = input('\nEnter the Client ID from the Spotify Developer App:\n')
    strClientSecret = input('\nEnter the Client Secret from the Spotify Developer App:\n')

    # Define the scopes your application requires
    listAuthScopesNeeded = ['playlist-modify-public', 'playlist-modify-private']

    # Redirect URI for your application (must be registered in your Spotify Developer Dashboard)
    STR_URL_REDIRECT = 'https://localhost'

    # Construct the authorization URL with the required parameters
    params = {
        'client_id': strClientId,
        'redirect_uri': STR_URL_REDIRECT,
        'scope': ' '.join(listAuthScopesNeeded),
        'response_type': 'code'
    }
    STR_URL_AUTH_PARAMS = STR_AUTHENTICATE_URL + '?' + urlencode(params)

    # Open the authorization URL in a browser to allow the user to authenticate and authorize your application
    print("\n[INFO] Please go to the following URL and authorize access:")
    print(f'[URL -->] {STR_URL_AUTH_PARAMS}')

    # After the user authorizes your application, they will be redirected to your redirect URI with an authorization code
    strCodeAuthorization = input("\nEnter the authorization code from the callback URL (found on the ?code URL param):\n")

    # Exchange the authorization code for an access token
    STR_URL_TOKEN_REQ = 'https://accounts.spotify.com/api/token'
    bodyParamsTokenData = {
        'grant_type': 'authorization_code',
        'code': strCodeAuthorization,
        'redirect_uri': STR_URL_REDIRECT,
        'client_id': strClientId,
        'client_secret': strClientSecret,
    }
    
    objResponseTokenAuth = requests.post(STR_URL_TOKEN_REQ, data=bodyParamsTokenData)

    if objResponseTokenAuth.status_code >= 400 and objResponseTokenAuth.status_code < 500:
        print(f'\n[ERROR] Status code returned: `{objResponseTokenAuth.status_code}` indicating that there is an issue generating a valid token credential. Please verify that your Client ID & Client Secret match your Spotify Developer App. Message from Spotify network request: "{objResponseTokenAuth.reason}"')
        print_error_exit_message()

    # Extract the access token from the response
    strAccessTokenGenerated = objResponseTokenAuth.json().get('access_token')

    # Now you can use the access token to make requests to the Spotify API with the specified scopes
    print("Valid Access token credential:\n", strAccessTokenGenerated)

    # TODO: fetch data of access token and write the credential to the json token key-val

    # with open('token.json', 'w') as file:
    #     data = {'access_token': access_token}

    #     json.dump(data, file)