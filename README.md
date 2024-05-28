# A2S
Free, interactive and lightweight python script to help migrate apple/audio playlist to Spotify. Checks for songs in Spotify playlist before inserting duplciates.

## Requirements
1. A Spotify Account
   1. Create a Spotify Developer account with your regular Spotify account.
   2. [Click here to visit Spotify Developer](https://developer.spotify.com/)
   3. Visit the "Dashboard" section and click "Create app"
   4. Name the title and add any description **but** use the same Redirect URI and API/SDKs. Then click "Save".
      ![](./photos/create_app_specs.png)
2. Python installation.
   1. [Download Python](https://www.python.org/downloads/)
   2. Program was run on version 3.12.2
3. A TSV of your playlist with at minimum the Artist name and the Song name as columns.
   1. Since this program is intended to migrate an Apple playlist to Spotify, I will use the ***Desktop*** Apple Music application to readily obtain the TSV of the data needed.
   2. Sign into Apple Music.
        ![](./photos/apple_music_sign_in.png)
   3. Signing in should prompt a syncing of library music/playlist from your phone.
      - If not you can go to Music (Top left) > Settings. Make sure the "Sync Library" option is toggled. Quit the application and reopen.
        ![](./photos/music_settings.png)
   4. With your playlist(s) synced, click the playlist, then click the first song and then select all tracks in the playlist with the short cut keys (CMD + A or Ctrl + A)
        ![](./photos/playlists_selection.png)
   5. Open a text editor or blank file in Notepad etc, paste the TSV and save it. You should see something like this if you followed the above steps. The red boxes from left to right are: the song name, and the artist name. Which is the minimum criteria needed in our TSV dump.
        ![](./photos/tsv_example.png)

## Running the Program
1. Be logged into Spofity in your Web browser executing the script.
2. Have the playlist created in Spotify.
3. Obtain a TSV of the songs you want to add to your spotify playlist. **2 Minimum fields needed are the Artist Name & Track Name**. Save this into the "PlaylistsInfo" directory of this project as a TSV file.
   1. See Step # 3 in the Requirements for getting a TSV from the desktop application for Apple Music.
4. Run ```python3 main.py``` in this project directory.
   1. Alternatively you can pass the --debug flag to record a txt file of the output stream of your interaction. ```python3 main.py --debug```
5. **Follow the console/output stream for instructions/directions!** 
   1. There will be some user input needed as the script progresses.
6. Disclaimer message will appear stating that you've met the requirements in order for the software to function as intended.
7. Then you'll be presented with a couple of options:
   1. **For running the program for the very 1st time**, you can choose option #1 to create the token json, fetch a credential token, and process the TSV to add to your spotify playlist.
   2. For subsequent uses, you'll most likely need to use option 3 after 1 hour since the token that Spotify provides is only valid for 1 hour. Option 4 can be used anytime when the token is valid.
8. Follow the prompts in the output stream to obtain the ```?code=``` param in the localhost URL when retreiving the access token credential.
   1. Probably best if you paste this into some sort of editor to easily extract the string value after ```?code=```. E.g. below
   ![](./photos/editor_url_code_example.png)
9. Then when prompted, you'll enter the name of your TSV playlist file that was saved in "PlaylistsInfo".
   ![TSV example saved in directory](./photos/playlist_tsv_saved.png)
   ![TSV file name input in program](./photos/playlist_tsv_input.png)
10. Then when prompted, you'll enter the name of your playlist ID.
    1. You can find this after the ```/playlists/``` in the URL. Example below
   ![Playlist ID Example](./photos/playlist_id_example.png)
11. If all goes well, songs will be inserted into playlists.
    1.  With the exception of songs that are already present in the playlist to avoid duplicates. This however should be indicated in the output stream.
12. Any issues with the software like network requests, invalid tokens should be logged into the output stream.