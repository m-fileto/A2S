import os
from datetime import datetime, timedelta
import requests
import json
from urllib.parse import urlencode, urlparse, parse_qs


def print_error_exit_message():
    print('\n\n\t\tExiting Program due to ERROR...\n\n')
    exit()

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
            fetch_token_credential(jsonData)
        elif jsonData['credential'] is None:
            print('[INFO] Fetching valid token credential since this is null. (Most likely due to first time program execution of lack of 1st success in auth request)')
            fetch_token_credential(jsonData)
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

def fetch_token_credential(jsonToken):
    # Spotify API endpoint for authorization
    STR_AUTHENTICATE_URL = 'https://accounts.spotify.com/authorize'

    jsonClient = None
    with open('client.json', 'r') as f:
        jsonClient = json.load(f)
    
    if jsonClient == None:
        print(f'[ERROR] "client.json" does not seem to exist or cannot be loaded. Make sure "client.json" exists and has keys populated.')
        print_error_exit_message()
        return 
    elif 'client_id' not in jsonClient:
        print(f'[ERROR] the key "client_id" is not present in "client.json". Cannot retreive auth token, please rerun program to add the key in "client.json"')
        print_error_exit_message()
        return
    elif jsonClient['client_id'] is None:
        print(f'[ERROR] the key "client_id" is present but does not have a valid value. Cannot retreive auth token, please rereun the program to update the key in "client.json"')
        print_error_exit_message()
        return 
    elif 'client_secret' not in jsonClient:
        print(f'[ERROR] the key "client_secret" is not present in "client.json". Cannot retreive auth token, please rerun program to add the key in "client.json"')
        print_error_exit_message()
        return
    elif jsonClient['client_secret'] is None:
        print(f'[ERROR] the key "client_secret" is present but does not have a valid value. Cannot retreive auth token, please rereun the program to update the key in "client.json"')
        print_error_exit_message()
        return 

    # Your application's client ID and client secret
    print('[INFO] Using the "client_id" and "client_secret" values from "client.json" for auth request.')
    strClientId = jsonClient['client_id']
    strClientSecret = jsonClient['client_secret']

    # Define the scopes your application requires
    # This allows us to modify both PUBLIC & PRIVATE playlists
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
    #   NEED TO LOGIN TO SPOTIFY IF NOT ALREADY LOGGED IN
    print("\n[INFO] (Need to be logged into Spotify) Please go to the following URL and authorize access (Note this will change the access code each time you make a new request):")
    print(f'\n[Visit URL Below]\n\n--->\t{STR_URL_AUTH_PARAMS}')

    # After the user authorizes your application, they will be redirected to your redirect URI with an authorization code
    strCodeAuthorization = input("\nEnter the authorization code provided by visiting the URL above (found on the value for `?code=` URL param):\n")

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
        return

    # Extract the access token from the response
    strAccessTokenGenerated = objResponseTokenAuth.json().get('access_token')

    # Now you can use the access token to make requests to the Spotify API with the specified scopes
    print("\nValid Access token credential:\n", strAccessTokenGenerated)

    # Succesfully got credential so update token json
    jsonToken['credential'] = strAccessTokenGenerated
    jsonToken['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('token.json', 'w') as file:
        json.dump(jsonToken, file, indent=4)

    print('\n[SUCCESS] Succesfully updated credential in "token.json"\n')