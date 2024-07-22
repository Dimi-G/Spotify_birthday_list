# creates a spotify playlist with the songs that were trending on the billboards during the user input date
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
from dotenv import load_dotenv
from pprint import pprint

def get_token(client_id, client_secret):
    """
    Retrieve an access token from Spotify using client credentials.
    
    Args:
        client_id (str): Spotify client ID
        client_secret (str): Spotify client secret
    
    Returns:
        str: The access token
    
    Raises:
        spotipy.SpotifyException: If there's an error getting the token
    """
    try:
        sp = spotipy.oauth2.SpotifyClientCredentials(
            client_id=client_id, 
            client_secret=client_secret
        )
        token_info = sp.get_access_token(check_cache=True)
        return token_info['access_token']
    except spotipy.SpotifyException as e:
        print(f"Error getting Spotify token: {e}")
        raise


#using spotipy library for easy access to spotify
load_dotenv()
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
USER_ID= os.environ.get("USER_ID")

#permission the scope for the modification of a playlist and create one
scope = "playlist-modify-private"
spot=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://example.com", scope=scope ))
playlist=spot.user_playlist_create(user=USER_ID, name = "Birthday Billboard for Corinna", public=False, collaborative=False, description= "Your tailored billboard")
playlist_id = playlist['id']
# user_info = spot.current_user()
# print(user_info)


#asking user for date input and accordingly scrapping the billboard song information
wanted_date= input("Which date do you want to musically travel to? Insert date in format YYYY-MM-DD:")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{wanted_date}")
response.raise_for_status()
soup=BeautifulSoup(response.content, "html.parser")
songs = soup.find_all("ul","lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p lrv-u-flex-direction-column@mobile-max")

title_list=[song.find("h3", id="title-of-a-story").text.strip() for song in songs]
artist_list=[song.find("span").text.strip() for song in songs]

#function for searching the spotify database for the songs and obtaining their id. In case a song is not found, it skips to the next
def search_track(title, artist):
        query = f"track:{title} artist:{artist}"
        results = spot.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track_info = results['tracks']['items'][0]
            #print(f"Found track: {track_info['name']} by {track_info['artists'][0]['name']} with id: {results['tracks']['items'][0]['id']}")
            #return track_info['id']
            return track_info['uri']
        else:
            pass

uri_list = []
#appending the songs' uri in the uri_list and adding them in the playlist
for song in title_list:
    index=title_list.index(song)
    uri=search_track(song, artist_list[index])
    uri_list.append(uri)
uri_list= [value for value in uri_list if value is not None]   
spot.playlist_add_items(playlist_id =playlist_id,items = uri_list)



