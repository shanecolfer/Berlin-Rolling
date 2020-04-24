import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from datetime import date

days_old = 19  # how many days old before removal


# Method to show tracks
def show_tracks(tracks):
    dates_added = []
    axed_trackIDs = []

    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s || %s || %s" % (i, track['artists'][0]['name'],
                                                track['name'], item['added_at'], track['id']))
        my_dict = {'id': track['id'], 'name': track['name'], 'date': item['added_at'][:-10]}
        dates_added.append(my_dict)

    print(dates_added)

    today = date.today()
    today = today.strftime("%Y-%m-%d")
    print("Today's date: ", today)

    for item in dates_added:
        if int(today[8:]) - int(item["date"][8:]) > days_old:  # THIS NUMBER DENOTES HOW OLD BEFORE REMOVAL IN DAYS
            print("This item is being removed: ", item["name"], " || Days since added: ", int(today[8:]) - int(item["date"][8:]))
            axed_trackIDs.append(item["id"])
    # This is (userID, playlistID, list of tracks to be deleted)
    userconn.user_playlist_remove_all_occurrences_of_tracks('11151496874', '4HB3J1hdYFY20nGCtuNeQs', axed_trackIDs)


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
playlist = sp.playlist('4HB3J1hdYFY20nGCtuNeQs')

print(playlist['name'])
print('  total tracks', playlist['tracks']['total'])

results = sp.playlist(playlist['id'], fields="tracks,next")
tracks = results['tracks']
show_tracks(tracks)

while tracks['next']:
    tracks = sp.next(tracks)
    show_tracks(tracks)
