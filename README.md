# A2S
Migrate apple playlist to spotify all with a python script


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

