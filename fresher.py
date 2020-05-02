import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from datetime import date
from datetime import datetime

days_old = 19  # how many days old before removal
rollingPlaylistID = '4HB3J1hdYFY20nGCtuNeQs'                        ####### '4HB3J1hdYFY20nGCtuNeQs'
backupPlaylistID = '6PaNSKAg1JeGh3ZzxWICDM'                         #### '6PaNSKAg1JeGh3ZzxWICDM'


# Method to show tracks
def show_tracks(tracks):
    dates_added = []
    axed_trackIDs = []
    num1 = 0

    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s || %s || %s" % (i, track['artists'][0]['name'],
                                                track['name'], item['added_at'], track['id']))
        my_dict = {'id': track['id'], 'name': track['name'], 'date': item['added_at'][:-10]}
        dates_added.append(my_dict)

    print(dates_added)

    today = date.today()
    todaystr = today.strftime("%Y-%m-%d")
    print("Today's date: ", today)

    # Go through dates added dict checking for songs older than 20 days, adding them to axed tracks if true
    for item in dates_added:
        # Current track date
        track_date = item["date"]
        print("Track Date = ", track_date)

        today = datetime.strptime(todaystr, "%Y-%m-%d")
        track_date = datetime.strptime(track_date, "%Y-%m-%d")

        # Get difference in days
        difference_in_days = today - track_date

        print("Difference in days = ", difference_in_days.days)

        # Check if the difference is bigger than our allowed difference
        if difference_in_days.days > days_old:  # THIS NUMBER DENOTES HOW OLD BEFORE REMOVAL IN DAYS
            print("This item is being removed: ", item["name"], " || Days since added: ", num1)
            axed_trackIDs.append(item["id"])

    # This is (userID, playlistID, list of tracks to be deleted) // DELETING THE TRACKS
    userconn.user_playlist_remove_all_occurrences_of_tracks('11151496874', rollingPlaylistID, axed_trackIDs)

    # Add deleted tracks to backup playlist (userID, playlistID, list of track IDs)
    if len(axed_trackIDs) > 0:
        userconn.user_playlist_add_tracks('11151496874', backupPlaylistID, axed_trackIDs)
        print("REMOVED TRACKS ADDED TO BACKUP PLAYLIST")
    else:
        print("NO TRACKS TO BE REMOVED")


print("Playlist Freshener")
print("------------------")
print("Currently removing songs from Rolling Jesh if they are %d days old" % (days_old+1))

scope = 'playlist-modify-public playlist-modify-private'
username = 'beanoclub@hotmail.com'
# Get credentials
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = util.prompt_for_user_token(username, scope)

if token:
    print("Auth Token received from Spotify Succesfully\n")
    userconn = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

# Get playlist by ID
playlist = sp.playlist(rollingPlaylistID)

print(playlist['name'])
print('  total tracks', playlist['tracks']['total'])

results = sp.playlist(playlist['id'], fields="tracks,next")
tracks = results['tracks']
show_tracks(tracks)

while tracks['next']:
    tracks = sp.next(tracks)
    show_tracks(tracks)
